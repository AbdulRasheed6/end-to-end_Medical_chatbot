from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings, load_cached_hugging_face_embeddings, init_pinecone_index
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from src.prompt import *
import os 


app= Flask(__name__)
load_dotenv()

PINECONE_API_KEY= os.environ.get('PINECONE_API_KEY2')
GEMINI_API_KEY= os.environ.get('GEMINI_API_KEY')


index_name='medicbot-v2'

os.environ["PINECONE_API_KEY"]= PINECONE_API_KEY

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


init_pinecone_index(PINECONE_API_KEY, index_name)

#embeddings= download_hugging_face_embeddings()
embeddings= load_cached_hugging_face_embeddings()


docsearch= PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever= docsearch.as_retriever(search_type='similarity', search_kwargs={"k":3})

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # or "gemini-1.5-pro"
    temperature=0.4,
    max_output_tokens=500,
    google_api_key= GEMINI_API_KEY

)


prompt= ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")

def index():
    return render_template('index.html')



@app.route("/get", methods=["POST"])
def chat():
    msg= request.form["msg"]
    input= msg
    print(input)
    response= rag_chain.invoke({"input": msg})
    print("Response :", response['answer'])
    return str(response["answer"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)