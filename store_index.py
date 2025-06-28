from src.helper import load_pdf_file, split_text, download_hugging_face_embeddings, load_cached_hugging_face_embeddings,upload_to_pinecone_parallel, init_pinecone_index
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv
import pickle


load_dotenv()

PINECONE_API_KEY= os.environ.get('PINECONE_API_KEY2')
GEMINI_API_KEY= os.environ.get('GEMINI_API_KEY')

index_name='medicbot-v2'

os.environ["PINECONE_API_KEY"]= PINECONE_API_KEY

init_pinecone_index(PINECONE_API_KEY, index_name)

#since the pdf  has been extracted out initially while testing , we can just comment it out
# extracted_data= load_pdf_file(data='Data/')
# Save
#with open('extracted_docs.pkl', 'wb') as f:
#    pickle.dump(extracted_data, f)

# Load
with open('extracted_docs.pkl', 'rb') as f:
    extracted_data = pickle.load(f)

#embeddings= download_hugging_face_embeddings()
embeddings= load_cached_hugging_face_embeddings()

chunks = split_text(extracted_data)  # extracted_data is your loaded documents

"""# STEP 2: Embed and upload in parallel, this could take a while that is why it is commented out
upload_to_pinecone_parallel(
    text_chunks=chunks,
    embeddings=embeddings,
    index_name='medicbot-v2',  
    batch_size=64,             
    max_workers=8              
)
"""

docsearch= PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

