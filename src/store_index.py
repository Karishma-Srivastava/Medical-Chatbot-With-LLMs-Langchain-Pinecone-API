from dotenv import load_dotenv
import os
from src.helpers import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from pinecone import Pinecone 
pinecone_api_key = PINECONE_API_KEY

pc = Pinecone(api_key=pinecone_api_key)

pc

from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(PINECONE_API_KEY)
index_name = "medical-chatbot"

# ✅ Check if index exists
existing_indexes = [index.name for index in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,  # Dimension of embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# ✅ Connect to the index
index = pc.Index(index_name)
print(f"Connected to index: {index_name}")

from langchain_community.vectorstores import Pinecone as PineconeVectorStore

# ✅ Step 1: Limit number of chunks (e.g., 10k or 12k)
LIMIT = 10000  # You can change to 12000 if stable
texts_chunk = texts_chunk[:LIMIT]

# ✅ Step 2: Optional – show how many will be embedded
print(f"Embedding and uploading {len(texts_chunk)} chunks to Pinecone...")

# ✅ Step 3: Embed + upload in batches to avoid connection drops
batch_size = 100  # safe size for Pinecone API
for i in range(0, len(texts_chunk), batch_size):
    batch = texts_chunk[i:i + batch_size]
    try:
        PineconeVectorStore.from_documents(
            documents=batch,
            embedding=embedding,
            index_name=index_name
        )
        print(f"✅ Uploaded batch {i // batch_size + 1} / {len(texts_chunk) // batch_size + 1}")
    except Exception as e:
        print(f"⚠️ Error in batch {i // batch_size + 1}: {e}")


# Load Existing index 

from langchain_community.vectorstores import Pinecone as PineconeVectorStore
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)