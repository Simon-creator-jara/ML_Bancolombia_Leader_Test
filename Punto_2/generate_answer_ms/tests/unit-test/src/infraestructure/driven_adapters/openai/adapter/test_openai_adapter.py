import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from openai import OpenAI
from src.domain.usecase.generate_answer.generate_answer_use_case import GenerateAnswerGateway
from src.infraestructure.driven_adapters.openai.adapter.openai_adapter import OpenAIQuestionImprover


@pytest.mark.asyncio
async def test_generate_answer_success():
    mock_openai_client = MagicMock(spec=OpenAI)
    
    mock_chat_completion_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "This is the improved answer based on the context."
    mock_chat_completion_response.choices = [MagicMock(message=mock_message)]
    
    mock_openai_client.chat.completions.create.return_value = mock_chat_completion_response

    improver = OpenAIQuestionImprover(client=mock_openai_client)

    question_text = "What is the plot of Inception?"
    answer_data = [
        ("Inception", "A thief who steals corporate secrets through use of dream-sharing technology...", "inception.jpg", "Cobb is a skilled thief", 0.05),
        ("The Matrix", "A computer hacker learns from mysterious rebels about the true nature of his reality...", "matrix.png", "Neo takes the red pill", 0.12)
    ]

    expected_context = (
        "[Movie: Inception]\nPlot: A thief who steals corporate secrets through use of dream-sharing technology...\nThe image associated with the movie Inception is: inception.jpg\n\n"
        "[Movie: The Matrix]\nPlot: A computer hacker learns from mysterious rebels about the true nature of his reality...\nThe image associated with the movie The Matrix is: matrix.png"
    )

    expected_messages = [
            {
                "role": "system",
                "content": (
                    """You are an assistant that answers only based on the given context. Always respond in spanish.
                    — Do not invent or assume anything beyond the given context."""
                )
            },
            {
                "role": "user",
                "content": f"""Based on the following movie data, answer the question {question_text}.
                            If the movie title is mentioned, match it exactly and return the associated information.
                            
                            {expected_context}
                            
                            """
            }
        ]

    result = await improver.generate(question_text, answer_data)

    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=expected_messages,
        temperature=0,
        max_tokens=500
    )
    
    assert result == "This is the improved answer based on the context."

@pytest.mark.asyncio
async def test_generate_answer_empty_context():
    mock_openai_client = MagicMock(spec=OpenAI)
    
    mock_chat_completion_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "No relevant information found."
    mock_chat_completion_response.choices = [MagicMock(message=mock_message)]
    
    mock_openai_client.chat.completions.create.return_value = mock_chat_completion_response

    improver = OpenAIQuestionImprover(client=mock_openai_client)

    question_text = "What is the plot of a non-existent movie?"
    answer_data = []

    expected_context = ""

    expected_messages = [
            {
                "role": "system",
                "content": (
                    """You are an assistant that answers only based on the given context. Always respond in spanish.
                    — Do not invent or assume anything beyond the given context."""
                )
            },
            {
                "role": "user",
                "content": f"""Based on the following movie data, answer the question {question_text}.
                            If the movie title is mentioned, match it exactly and return the associated information.
                            
                            {expected_context}
                            
                            """
            }
        ]

    result = await improver.generate(question_text, answer_data)

    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=expected_messages,
        temperature=0,
        max_tokens=500
    )
    assert result == "No relevant information found."


@pytest.mark.asyncio
async def test_generate_answer_openai_api_error():
    mock_openai_client = MagicMock(spec=OpenAI)
    
    mock_openai_client.chat.completions.create.side_effect = Exception("OpenAI API is down!")

    improver = OpenAIQuestionImprover(client=mock_openai_client)

    question_text = "What is the plot of Inception?"
    answer_data = [("Inception", "Plot A", "imageA", "chunkA", 0.1)]

    with pytest.raises(Exception, match="OpenAI API is down!"):
        await improver.generate(question_text, answer_data)

    mock_openai_client.chat.completions.create.assert_called_once()