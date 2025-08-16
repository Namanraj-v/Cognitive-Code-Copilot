
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class CodeInput(BaseModel):
    code: str
    refactor_style: str = Field(..., description="The style of refactoring to apply (e.g., readability, conciseness)")

class AnalysisResult(BaseModel):
    metrics: Dict[str, Any]
    issues: List[str]

class RefactorResponse(BaseModel):
    original_code: str
    refactored_code: str
    documentation: str
    unit_tests: str
    analysis_report: Dict[str, Any]

# --- Chat Schemas (New) ---
class ChatInput(BaseModel):
    code: str
    history: List[Dict[str, str]]
    question: str

class ChatResponse(BaseModel):
    answer: str