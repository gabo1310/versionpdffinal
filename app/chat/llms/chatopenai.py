from langchain.chat_models import ChatOpenAI
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

def build_llm(chat_args, model_name, temperature=0.2):
    return ChatOpenAI(
        streaming=chat_args.streaming,
        model_name=model_name,
        temperature=temperature  
    )