from langchain.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from app.chat.models import ChatArgs
from app.chat.vector_store import retriever_map
from app.chat.llms.chatopenai import build_llm
#from app.chat.llms.claudeai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import(
    set_conversation_components,
    get_conversation_components
)
import random
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.score import random_component_by_score

from app.chat.tracing.langfuse import langfuse
from langfuse.model import CreateTrace
import os
from langchain_anthropic import ChatAnthropic

from langchain.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from app.chat.models import ChatArgs
from app.chat.vector_store import retriever_map
#from app.chat.llms.claudeai import build_llm
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import(
    set_conversation_components,
    get_conversation_components
)
import random
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.score import random_component_by_score
from langchain.prompts import PromptTemplate

import os
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')


def select_component(
    component_type, component_map, chat_args
):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)


def build_chat(chat_args: ChatArgs):
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)

    print("###############################")
    print(f"memoria:{memory_name}, llm: {llm_name}, retriever: {retriever_name}")
    print("###############################")
    
    set_conversation_components(chat_args.conversation_id, llm=llm_name, retriever=retriever_name, memory=memory_name)

    if llm_name == "claude-3":
        condense_question_llm = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
    else:
        condense_question_llm = ChatOpenAI(streaming=False, temperature=0)  # Asegúrate de establecer la temperatura a 0



    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata # Usa el prompt personalizado
    )