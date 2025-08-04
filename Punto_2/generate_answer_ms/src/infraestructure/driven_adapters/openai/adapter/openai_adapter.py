from openai import OpenAI
import asyncio
from src.domain.usecase.generate_answer.generate_answer_use_case import GenerateAnswerGateway


class OpenAIQuestionImprover(GenerateAnswerGateway):
    def __init__(self, client: OpenAI):
        self.client = client

    async def generate(self, question: str, answer: list) -> str:

        context = "\n\n".join([
            f"[Movie: {title}]\nPlot: {plot}\nThe image associated with the movie {title} is: {image}" 
            for title, plot, image, chunk_text, distance in answer
        ])
        print(context)
        messages = [
            {
                "role": "system",
                "content": (
                    """You are an assistant that answers only based on the given context. Always respond in spanish.
                    — Do not invent or assume anything beyond the given context."""
                )
            },
            {
                "role": "user",
                "content": f"""Based on the following movie data, answer the question {question}.
                            If the movie title is mentioned, match it exactly and return the associated information.
                            
                            {context}
                            
                            """
            }
        ]

        response = await asyncio.to_thread(self.client.chat.completions.create,
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()
