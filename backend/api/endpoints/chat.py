from fastapi import APIRouter, HTTPException
from backend.models.schemas import ChatInput, ChatResponse
from backend.services import llm_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(chat_input: ChatInput):
    try:
        # Construct a single, comprehensive prompt for the LLM
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_input.history])

        prompt = f"""
        You are a "Code-Aware Copilot". Your role is to assist a user with their Python code.

        **Current Code Context:**
        ```python
        {chat_input.code}
        ```

        **Conversation History:**
        {history_str}

        **User's Latest Question:**
        {chat_input.question}

        Based on all the information above (the current code, the history, and the new question), provide a helpful response.
        If the user asks you to modify the code, provide ONLY the updated code block in your response.
        Otherwise, answer their question clearly.
        """
        
        ai_response = llm_service.generate_completion(prompt)
        
        return ChatResponse(answer=ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))