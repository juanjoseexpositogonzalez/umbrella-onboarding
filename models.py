import os
from enum import StrEnum

from decouple import config


def prepare_environmnet() -> None:
    """
    Prepare the environment for the AI model.
    This function can be used to set up any necessary configurations or
    environment variables before using the AI model.
    """
    # Placeholder for environment preparation logic
    os.environ["OPENAI_API_KEY"] = config(  # type: ignore[assignment]
        "OPENAI_API_KEY",
    )  # type: ignore[assignment]
    os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")  # type: ignore[assignment]
    os.environ["LANGSMITH_API_KEY"] = config("LANGSMITH_API_KEY")  # type: ignore[assignment]
    os.environ["LANGCHAIN_TRACING_V2"] = config("LANGCHAIN_TRACING_V2")  # type: ignore[assignment]
    os.environ["LANGCHAIN_PROJECT"] = config("LANGCHAIN_PROJECT")  # type: ignore[assignment]


class AIModel(StrEnum):
    """
    Enum for AI models.
    """

    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    LLAMA_VERSATILE = "llama-3.3-70b-versatile"
