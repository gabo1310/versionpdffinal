from langchain.embeddings import OpenAIEmbeddings
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

embeddings = OpenAIEmbeddings()