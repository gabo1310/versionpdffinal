import os
import pinecone
from langchain.vectorstores import Pinecone
from app.chat.embeddings.openai import embeddings
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')


pinecone.Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME")
)

vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

def build_retriever(chat_args, k):
    search_kwargs = {
        "k": k
    }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )




# ##constructor 
# def build_retriever(chat_args, k):
#     search_kwargs = {
#         "filter": { "pdf_id": chat_args.pdf_id },
#         #"filter": { "$in": chat_args.pdf_id },
#         "k": k
#     }
#     return vector_store.as_retriever(
#         search_kwargs=search_kwargs
#     )
    
# def build_retriever(chat_args, k, pdf_ids_to_search):
#     search_kwargs = {"filter": {"pdf_id": {"$in": pdf_ids_to_search}}, "k": k}
#     return vector_store.as_retriever(search_kwargs=search_kwargs)

