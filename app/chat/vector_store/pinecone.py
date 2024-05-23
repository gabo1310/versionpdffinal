# import os
# import pinecone
# from langchain.vectorstores import Pinecone as LangchainPinecone
# from app.chat.embeddings.openai import embeddings
# import warnings

# # Ignorar todas las advertencias de LangChain deprecado
# warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

# # Inicializar Pinecone
# pc = pinecone.Pinecone(
#     api_key=os.getenv("PINECONE_API_KEY"),
#     environment=os.getenv("PINECONE_ENV_NAME")
# )

# # Usar el índice existente
# vector_store = LangchainPinecone.from_existing_index(
#     os.getenv("PINECONE_INDEX_NAME"), embeddings
# )

# def build_retriever(chat_args, k, pdf_ids_to_search=None):
#     print("###############################################") 
#     print(f"PDF IDs to search: {pdf_ids_to_search}") 
#     print("###############################################") 
#     if pdf_ids_to_search is None:
#         pdf_ids_to_search = [chat_args.pdf_id]
#     print(f"PDF IDs to search: {pdf_ids_to_search}")  # Para depuración
#     search_kwargs = {"filter": {"pdf_id": {"$in": pdf_ids_to_search}}, "k": k}
#     return vector_store.as_retriever(
#         search_kwargs=search_kwargs
#     )

# def build_retriever(chat_args, k, pdf_ids_to_search=None):
#     # Forzar el uso de una ID específica
#     pdf_ids_to_search = ["d6e55076-1089-4680-a4b5-3954944d4a4c"]
#     print(f"PDF IDs to search: {pdf_ids_to_search}")  # Para depuración
#     search_kwargs = {"filter": {"pdf_id": {"$in": pdf_ids_to_search}}, "k": k}
#     return vector_store.as_retriever(
#         search_kwargs=search_kwargs
#     )




# def build_retriever(chat_args, k, pdf_ids_to_search=None):
#     print(pdf_ids_to_search)
#     search_kwargs = {"k": k}
#     if pdf_ids_to_search:
#         search_kwargs["filter"] = {"pdf_id": {"$in": pdf_ids_to_search}}
#     return vector_store.as_retriever(
#         search_kwargs=search_kwargs
#     )


###########################################################
#el mismo pdf dentro: 
# def build_retriever(chat_args, k):
#     print(chat_args.pdf_id)
#     search_kwargs = {
#         "filter": { "pdf_id": chat_args.pdf_id },
#         "k": k
#     }
#     return vector_store.as_retriever(
#         search_kwargs=search_kwargs
#     )
    
import os
import pinecone
from langchain.vectorstores import Pinecone as LangchainPinecone
from app.chat.embeddings.openai import embeddings
import warnings
from flask import session

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

# Inicializar Pinecone
pc = pinecone.Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME")
)

# Usar el índice existente
vector_store = LangchainPinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

def build_retriever(chat_args, k):
    pdf_ids_to_search = session.get('selected_pdfs', [chat_args.pdf_id])  # Obtener las IDs de la sesión
    if isinstance(pdf_ids_to_search, str):
        pdf_ids_to_search = [pdf_ids_to_search]  # Convertir a lista si es una cadena
    # print("#############################")
    # print(f"PDF IDs to search: {pdf_ids_to_search}")  # Para depuración
    # print("#############################")
    
    search_kwargs = {"filter": {"pdf_id": {"$in": pdf_ids_to_search}}, "k": k}
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )

