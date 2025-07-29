from pydantic import BaseModel
from typing import Optional, List

class answer(BaseModel):
    answer: List

class GenerateAnswerRequest(BaseModel):
    question: str
    answer: List
