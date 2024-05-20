#se va a crear una pequeña cadena
import os
from pinecone import Pinecone
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain.chains import RetrievalQA, LLMChain, SequentialChain, VectorDBQA
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from langchain_community.document_loaders import ReadTheDocsLoader 
# Index name in Pinecone
from langchain.chains import RetrievalQA
from tqdm.auto import tqdm
from uuid import uuid4
from pinecone import Pinecone
from getpass import getpass
from langchain.embeddings.openai import OpenAIEmbeddings
#from datasets import load_dataset
from getpass import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from dotenv import load_dotenv
from langchain.memory import ConversationSummaryMemory ,ConversationBufferMemory, FileChatMessageHistory
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.vectorstores.chroma import Chroma
import colorama
import sys
import io
from app.chat.vector_store.pinecone import vector_store
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """
    Generar y almacenar embeddings para el PDF dado

    1. Extraer texto del PDF especificado.
    2. Dividir el texto extraído en fragmentos manejables.
    3. Generar un embedding para cada fragmento.
    4. Persistir los embeddings generados.

    """
    ##-------------------------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2048,
        chunk_overlap = 1024
    )
    
    ##-------------------------------------
    
    # text_splitter = CharacterTextSplitter(
    #     chunk_size = 2048,
    #     chunk_overlap = 1024
    # )
    
    
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load_and_split(text_splitter)
    
    
    for doc in docs:
        doc.metadata = {
            "page": doc.metadata["page"],
            "text": doc.page_content,
            "pdf_id": pdf_id

        }

    
    vector_store.add_documents(docs)
    #print(docs)


