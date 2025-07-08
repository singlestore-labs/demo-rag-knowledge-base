import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

openai_embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-ada-002"
)


def embed_documents(texts: list[str]) -> list[list[float]]:
    return openai_embeddings.embed_documents(texts)


def embed_query(text: str) -> list[float]:
    return openai_embeddings.embed_query(text)
