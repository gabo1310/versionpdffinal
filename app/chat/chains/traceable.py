from langfuse.model import CreateTrace
from app.chat.tracing.langfuse import langfuse
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

class TraceableChain:
    def __call__(self, *args, **kwargs):
        trace = langfuse.trace(
            CreateTrace(
                id=self.metadata["conversation_id"],
                metadata=self.metadata
            )
        )   
        callbacks = kwargs.get("callbacks", [])
        callbacks.append(trace.getNewHandler())
        kwargs["callbacks"] = callbacks
        return super().__call__(*args, **kwargs)
