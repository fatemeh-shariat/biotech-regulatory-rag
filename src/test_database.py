import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# 1. Insert a test document
doc = (
    client.table("documents")
    .insert(
        {
            "title": "Test document",
            "source_type": "test",
            "file_name": "test_document.pdf",
            "total_pages": 1,
        }
    )
    .execute()
)
doc_id = doc.data[0]["id"]
print("Inserted document id:", doc_id)

# 2. Insert a test chunk with a dummy embedding (1536 numbers)
chunk = (
    client.table("chunks")
    .insert(
        {
            "document_id": doc_id,
            "chunk_index": 0,
            "page_number": 1,
            "content": "This is a test chunk about FDA guidance.",
            "embedding": [0.01] * 1536,
        }
    )
    .execute()
)
print("Inserted chunk id:", chunk.data[0]["id"])

# 3. Read the chunk back
rows = (
    client.table("chunks")
    .select("id, document_id, page_number, content")
    .eq("document_id", doc_id)
    .execute()
)
print("Read back:", rows.data)

# 4. Clean up: deleting the document also deletes its chunks (cascade)
client.table("documents").delete().eq("id", doc_id).execute()
print("Test data cleaned up")