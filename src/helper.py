from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
import shutil
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from langchain_pinecone import PineconeVectorStore
from tqdm import tqdm
from pinecone import ServerlessSpec
import json



#extract data from the pdf file
def load_pdf_file(data):
    loader= DirectoryLoader(data,
                           glob="*.pdf",
                        loader_cls=PyPDFLoader)
    documents=loader.load()

    return documents


def init_pinecone_index(api_key, index_name, dimension=384):
    pc = Pinecone(api_key=api_key)

    if index_name not in [idx.name for idx in pc.list_indexes().indexes]:
        print(f"Creating index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    else:
        print(f"Index '{index_name}' already exists.")

    return index_name



# split the data into text chunks
def split_text(documents, chunk_size=500, chunk_overlap=20):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


def download_hugging_face_embeddings():
    cache_dir = './model_cache'

    # Clear existing cache (optional, to force re-download)
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        cache_folder=cache_dir  
    )
    return embeddings


def load_cached_hugging_face_embeddings():
    cache_dir = './model_cache'

    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        cache_folder=cache_dir  # It will now load from here without re-downloading
    )
    return embeddings


# Global lock to prevent concurrent writes
write_lock = Lock()

def load_uploaded_batch_ids(file_path="uploaded_batches.json"):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                if not content:
                    return set()
                return set(json.loads(content))
        except json.JSONDecodeError:
            print("JSON corrupted, starting fresh.")
            os.remove(file_path)
            return set()
    return set()


def save_uploaded_batch_ids(uploaded_ids, file_path="uploaded_batches.json"):
    with write_lock:
        with open(file_path, "w") as f:
            json.dump(list(uploaded_ids), f)


def upload_to_pinecone_parallel(text_chunks, embeddings, index_name, batch_size=64, max_workers=8):
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    uploaded_batch_ids = load_uploaded_batch_ids()

    def upload_batch(batch_id, batch):
        if str(batch_id) in uploaded_batch_ids:
            return  # Skip already uploaded
        try:
            docsearch.add_documents(batch)
            with write_lock:
                uploaded_batch_ids.add(str(batch_id))
                save_uploaded_batch_ids(uploaded_batch_ids)
        except Exception as e:
            print(f"Failed batch upload {batch_id}: {e}")

    # Create batches
    batches = [
        (i, text_chunks[i:i + batch_size])
        for i in range(0, len(text_chunks), batch_size)
    ]

    print(f" Resumable parallel upload with {max_workers} workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(
            executor.map(lambda args: upload_batch(*args), batches),
            total=len(batches),
            desc="Uploading"
        ))

    print(" Finished uploading all batches.")
