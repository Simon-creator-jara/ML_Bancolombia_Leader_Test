from openai import OpenAI
import asyncio
from src.domain.usecase.improve_question.improve_question_use_case import QuestionImproverGateway


class OpenAIQuestionImprover(QuestionImproverGateway):
    def __init__(self, client: OpenAI):
        self.client = client

    async def improve(self, question: str) -> str:
        prompt = (
            "You are a helpful assistant…\n\n"
            f"Original question: \"{question}\"\n\n"
            "Improved version:"
        )
        resp = await asyncio.to_thread(self.client.chat.completions.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You improve questions for retrieval."},
                {"role": "user",   "content": prompt},
            ],
            temperature=0,
            max_tokens=512
        )
        return resp.choices[0].message.content.strip()
