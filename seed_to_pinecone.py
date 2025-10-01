# seed_to_pinecone.py (updated version)
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import openai
from seed import monster_entries
import time

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = PINECONE_INDEX

existing_indexes = pc.list_indexes().names()
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print(f"Created index {index_name}")
    time.sleep(10)
else:
    print(f"Index {index_name} already exists")


index = pc.Index(index_name)


def get_embedding(text):
    response = openai.embeddings.create(model="text-embedding-ada-002", input=text)
    return response.data[0].embedding


def load_entries():
    for i, entry in enumerate(monster_entries):
        print(f"Processing entry {i+1}/{len(monster_entries)}: {entry['title']}")

        text_to_embed = f"{entry['title']}. {entry['text']}"

        embedding = get_embedding(text_to_embed)

        index.upsert(
            vectors=[
                {
                    "id": f"entry_{i:03d}",
                    "values": embedding,
                    "metadata": {
                        "title": entry["title"],
                        "author": entry["author"],
                        "date": entry["date"],
                        "full_text": entry["text"],
                    },
                }
            ]
        )

        time.sleep(0.5)

    print(f"\nSuccessfully loaded {len(monster_entries)} entries!")
    print(f"Index stats: {index.describe_index_stats()}")


if __name__ == "__main__":
    load_entries()
