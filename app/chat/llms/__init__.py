from .chatopenai import build_llm
from .chatclaudeai import build_llm_clau
from functools import partial
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

llm_map = {
    #"gpt-4": partial(build_llm, model_name="gpt-4", temperature=0)
    #"gpt-3.5-turbo":partial(build_llm, model_name="gpt-3.5-turbo", temperature=0)
    "gpt-4o": partial(build_llm, model_name="gpt-4o", temperature=0)
    #"claude-3": partial(build_llm_clau, model_name="claude-3-opus-20240229")
}

# llm_map_clau = {
#     "claude-3": partial(build_llm_clau, model_name="claude-3-opus-20240229")
# }SS

