from openai import OpenAI
import asyncio
from src.domain.usecase.improve_question.improve_question_use_case import QuestionImproverGateway


class OpenAIQuestionImprover(QuestionImproverGateway):
    def __init__(self, client: OpenAI):
        self.client = client

    async def improve(self, question: str) -> str:
        prompt = f"""
        You are part of an information retrieval system. You must classify the user's intent and act according to the following instructions:
        
        1. If the message is a real question (it seeks information about movies, your databe knowledge it's about movies'), tag it as [real] and rephrase the question to make it clearer and more useful for semantic search, do this in English.
        2. If it is a greeting, farewell, casual conversation, tag it as [greeting], [farewell], or [smalltalk], and respond appropriately in Spanish yourself. Also if the user asks like cómo me puedes ayudar?, qué puedes hacer por mi? or so on he is trying to get information about what kind of questions you can respond. Respond that you only can provide infromation about movies in spanish.
        3. If the message is a question about your behaviour or what you can do, tag it as [smalltalk] and respond with: "Puedo ayudarte con información acerca de peliculas." . Also, you have to identify similar questions and respond with the same answer.
        4. If the message is a question unrelated with your behaviour or what you can do or what you can help, tag it as [other] and respond with: "Lo siento, no puedo ayudarte con eso."
        
        Never make up information. Do not modify greetings or casual comments.
        
        The user's message is in **Spanish** and must be interpreted in **Spanish** and answered in **English**.
        
        User message: "{question}"
        
        Generated response:
        """.strip()

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
