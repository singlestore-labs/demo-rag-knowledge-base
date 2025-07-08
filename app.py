import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from openai import OpenAI

from lib.db import db
from lib.embed import embed_query

load_dotenv()

app = FastAPI()
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def vector_search(query_embedding: list[float], top_k: int = 3) -> list[dict]:
    """
    Execute a k-NN similarity search against the 'knowledge_base' table in SingleStore.
    Uses the '<*>' operator for dot-product similarity (assumes embeddings are normalized).
    """
    with db.cursor() as cursor:
        cursor.execute(
            "SET @query_vec = %s :> VECTOR(%s);",
            (str(query_embedding), len(query_embedding))
        )

        cursor.execute(
            """
            SELECT id, source, content, embedding <*> @query_vec AS similarity
            FROM knowledge_base
            ORDER BY similarity DESC
            LIMIT %s;
            """,
            (top_k,)
        )

        return cursor.fetchall()


@app.get("/ask")
def ask(
    query: str = Query(
        ...,
        min_length=1,
        max_length=512,
        description="The user question to be answered using vector-search context."
    )
):
    try:
        query_embedding = embed_query(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    try:
        search_results = vector_search(query_embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector search error: {e}")

    if not search_results:
        return {"answer": "No relevant data found."}

    context = "\n---\n".join(search_result["content"] for search_result in search_results)

    try:
        system_role = "You are a helpful AI assistant. Use the provided context excerpts to answer the user's question."

        content = f"""
            User Question: {query}\n
            Context: {context}
        """

        completion = llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": content}
            ]
        )

        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

    return {
        "question": query,
        "answer": answer,
        "search_results": search_results
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
