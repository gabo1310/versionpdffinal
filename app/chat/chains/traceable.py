from langfuse.model import CreateTrace
from app.chat.tracing.langfuse import langfuse

class TraceableChain:
    def __call__(self, *args, **kwargs):
        trace = langfuse.trace(
            CreateTrace(
                id=self.metadata["conversation_id"],
                metadata=self.metadata
            )
        )   
        # Asegúrate de que callbacks sea una lista
        callbacks = kwargs.get("callbacks", [])
        if callbacks is None:
            callbacks = []
        new_handler = trace.getNewHandler()
        if new_handler is not None:
            callbacks.append(new_handler)
        kwargs["callbacks"] = callbacks
        return super().__call__(*args, **kwargs)
