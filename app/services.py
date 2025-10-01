# app/services.py
import os
from pinecone import Pinecone
import openai
from dotenv import load_dotenv
from app.constants import PINECONE_INDEX

load_dotenv()

# Initialize clients once
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(PINECONE_INDEX)
openai.api_key = os.getenv("OPENAI_API_KEY")


class SearchService:
    @staticmethod
    def get_embedding(text: str):
        response = openai.embeddings.create(model="text-embedding-ada-002", input=text)
        return response.data[0].embedding

    @staticmethod
    def search_entries(query: str, limit: int = 10):
        query_embedding = SearchService.get_embedding(query)

        results = index.query(
            vector=query_embedding, top_k=limit, include_metadata=True
        )

        entries = []
        for match in results["matches"]:
            entries.append(
                {
                    "id": match["id"],
                    "score": match["score"],
                    "title": match["metadata"].get("title"),
                    "author": match["metadata"].get("author"),
                    "date": match["metadata"].get("date"),
                    "excerpt": match["metadata"].get("full_text")[:200] + "...",
                }
            )

        return entries
