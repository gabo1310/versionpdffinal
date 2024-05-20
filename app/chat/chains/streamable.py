from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler
from flask import current_app
# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')

class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()
            self(input, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()
        
        while True:
            token = queue.get()
            if token is None:
                break
            yield token
            
            
            #revisar aca los tokens solo estan recibiendo al inicio