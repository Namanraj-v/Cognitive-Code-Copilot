from fastapi import APIRouter, HTTPException
from backend.models.schemas import CodeInput, RefactorResponse
from backend.services import code_analyzer, llm_service, rag_service

router = APIRouter()

def get_prompt_for_style(style: str, code: str, context: str) -> str:
    """Returns a specific LLM prompt based on the chosen refactoring style."""
    
    prompts = {
        "readability": f"""
        **Context:** {context}
        **Task:** Based on the context, refactor the following Python code to prioritize **maximum readability and clarity**. 
        Break it down into smaller, well-named functions. Add comprehensive Google-style docstrings and type hints.
        
        **Original Code:**
        ```python
        {code}
        ```
        **Your response should be ONLY the refactored Python code block.**
        """,
        "conciseness": f"""
        **Context:** {context}
        **Task:** Based on the context, refactor the following Python code to be as **concise and Pythonic as possible**.
        Use modern Python features like list comprehensions, ternary operators, and other idioms where appropriate, without sacrificing essential readability. Add minimal docstrings and type hints.
        
        **Original Code:**
        ```python
        {code}
        ```
        **Your response should be ONLY the refactored Python code block.**
        """,
        "documentation": f"""
        **Task:** Do not refactor the logic of the code. Your only task is to **add comprehensive Google-style docstrings and type hints** to the following Python code.
        
        **Original Code:**
        ```python
        {code}
        ```
        **Your response should be ONLY the commented and type-hinted Python code block.**
        """
    }
    return prompts.get(style, prompts['readability']) # Default to readability

@router.post("/refactor", response_model=RefactorResponse)
async def refactor_code(code_input: CodeInput):
    try:
        # Step 1: Analyze the code
        analysis = code_analyzer.analyze_code(code_input.code)
        
        # Step 2: Retrieve relevant context using RAG
        smell = analysis['identified_smells'][0] if analysis['identified_smells'] else None
        rag_context = rag_service.get_rag_context(smell)

        # Step 3: Get the correct prompt based on user's choice
        refactor_prompt = get_prompt_for_style(code_input.refactor_style, code_input.code, rag_context)
        refactored_code = llm_service.generate_completion(refactor_prompt)
        
        # Step 4: Generate unit tests for the NEW code
        test_prompt = f"""
        **Task:** Generate a set of `pytest` unit tests for the following Python function.
        **Function:**
        ```python
        {refactored_code}
        ```
        **Your response should be ONLY the Python code block for the tests.**
        """
        unit_tests = llm_service.generate_completion(test_prompt)

        return RefactorResponse(
            original_code=code_input.code,
            refactored_code=refactored_code,
            documentation="Generated from refactored code.",
            unit_tests=unit_tests,
            analysis_report=analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))