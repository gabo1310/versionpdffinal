# warnings_filter.py
import warnings

# Ignorar todas las advertencias de LangChain deprecado
warnings.filterwarnings("ignore", category=DeprecationWarning, module='langchain_core._api.deprecation')


from app.web import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
