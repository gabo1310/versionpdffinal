"""
Este módulo define un blueprint para manejar las rutas relacionadas 
con las conversaciones de chat.
Incluye rutas para listar, crear conversaciones y 
agregar mensajes a una conversación específica.
Utiliza decoradores para verificar la autenticación del usuario y cargar modelos.
"""

from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat import build_chat, ChatArgs

# Define el blueprint con el prefijo de URL /api/conversations
bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")

# Ruta para listar todas las conversaciones asociadas a un PDF específico
@bp.route("/", methods=["GET"])
@login_required  # Verifica que el usuario esté autenticado
@load_model(Pdf, lambda r: r.args.get("pdf_id"))  # Carga el modelo PDF basado en el ID proporcionado en la solicitud
def list_conversations(pdf):
    return [c.as_dict() for c in pdf.conversations]  # Retorna las conversaciones asociadas al PDF como una lista de diccionarios

# Ruta para crear una nueva conversación asociada a un PDF específico
@bp.route("/", methods=["POST"])
@login_required  # Verifica que el usuario esté autenticado
@load_model(Pdf, lambda r: r.args.get("pdf_id"))  # Carga el modelo PDF basado en el ID proporcionado en la solicitud
def create_conversation(pdf):
    conversation = Conversation.create(user_id=g.user.id, pdf_id=pdf.id)  # Crea una nueva conversación

    return conversation.as_dict()  # Retorna la nueva conversación como un diccionario

# Ruta para agregar un mensaje a una conversación específica
@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required  # Verifica que el usuario esté autenticado
@load_model(Conversation)  # Carga el modelo Conversation basado en el ID proporcionado en la solicitud
def create_message(conversation):
    input = request.json.get("input")  # Obtiene el mensaje de entrada de la solicitud JSON
    streaming = request.args.get("stream", False)  # Obtiene el parámetro de streaming de la solicitud

    pdf = conversation.pdf
    prompt = input  # Usa el input proporcionado como prompt
    additional_prompt = "Que la respuesta no supere las 15 palabras."  # Aquí añadimos el additional_prompt

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        pdf_id=pdf.id,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "user_id": g.user.id,
            "pdf_id": pdf.id,
        },
        prompt=prompt,
        additional_prompt=additional_prompt  # Proporcionamos el additional_prompt
    )

    chat = build_chat(chat_args)  # Construye el objeto de chat con los argumentos proporcionados

    if not chat:
        return "Chat not yet implemented!"  # Retorna un mensaje si el chat no está implementado

    if streaming:
        return Response(
            stream_with_context(chat.stream(input)), mimetype="text/event-stream"
        )  # Retorna la respuesta en streaming
    else:
        return jsonify({"role": "assistant", "content": chat.run(input)})  # Retorna la respuesta del chat en formato JSON

######################################

"""
Este módulo define un blueprint para manejar las rutas relacionadas 
con las conversaciones de chat.
Incluye rutas para listar, crear conversaciones y 
agregar mensajes a una conversación específica.
Utiliza decoradores para verificar la autenticación del usuario y cargar modelos.
"""

from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat import build_chat, ChatArgs

# Define el blueprint con el prefijo de URL /api/conversations
bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")

# Ruta para listar todas las conversaciones asociadas a un PDF específico
@bp.route("/", methods=["GET"])
@login_required  # Verifica que el usuario esté autenticado
@load_model(Pdf, lambda r: r.args.get("pdf_id"))  # Carga el modelo PDF basado en el ID proporcionado en la solicitud
def list_conversations(pdf):
    return [c.as_dict() for c in pdf.conversations]  # Retorna las conversaciones asociadas al PDF como una lista de diccionarios

# Ruta para crear una nueva conversación asociada a un PDF específico
@bp.route("/", methods=["POST"])
@login_required  # Verifica que el usuario esté autenticado
@load_model(Pdf, lambda r: r.args.get("pdf_id"))  # Carga el modelo PDF basado en el ID proporcionado en la solicitud
def create_conversation(pdf):
    conversation = Conversation.create(user_id=g.user.id, pdf_id=pdf.id)  # Crea una nueva conversación

    return conversation.as_dict()  # Retorna la nueva conversación como un diccionario

# Ruta para agregar un mensaje a una conversación específica
@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required  # Verifica que el usuario esté autenticado
@load_model(Conversation)  # Carga el modelo Conversation basado en el ID proporcionado en la solicitud
def create_message(conversation):
    input = request.json.get("input")  # Obtiene el mensaje de entrada de la solicitud JSON
    streaming = request.args.get("stream", False)  # Obtiene el parámetro de streaming de la solicitud

    pdf = conversation.pdf
    prompt = input  # Usa el input proporcionado como prompt
    additional_prompt = "Responde en la menor cantidad de palabras posibles."  # Aquí añadimos el additional_prompt

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        pdf_id=pdf.id,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "user_id": g.user.id,
            "pdf_id": pdf.id,
        },
        prompt=prompt,
        additional_prompt=additional_prompt  # Proporcionamos el additional_prompt
    )

    chat = build_chat(chat_args)  # Construye el objeto de chat con los argumentos proporcionados

    if not chat:
        return "Chat not yet implemented!"  # Retorna un mensaje si el chat no está implementado

    if streaming:
        return Response(
            stream_with_context(chat.stream(input)), mimetype="text/event-stream"
        )  # Retorna la respuesta en streaming
    else:
        return jsonify({"role": "assistant", "content": chat.run(input)})  # Retorna la respuesta del chat en formato JSON


###################################################

def build_chat(chat_args: ChatArgs):
    """
    Construye el chat utilizando los componentes seleccionados y la cadena de recuperación conversacional con streaming.

    :param chat_args: Argumentos del chat que contienen el ID de la conversación y otros metadatos

    :return: Instancia de StreamingConversationalRetrievalChain configurada con los componentes seleccionados
    """
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)

    print("###############################")
    print(f"memoria: {memory_name}, llm: {llm_name}, retriever: {retriever_name}")
    print("###############################")

    set_conversation_components(chat_args.conversation_id, llm=llm_name, retriever=retriever_name, memory=memory_name)

    additional_prompt = chat_args.additional_prompt

    # Construimos el mensaje para el LLM sin duplicar la pregunta
    initial_prompt = f"{additional_prompt}\nPregunta del usuario: {chat_args.prompt}"

    if llm_name == "claude-3":
        condense_question_llm = ChatAnthropic(
            streaming=chat_args.streaming,
            model_name="claude-3-opus-20240229"
        )
    else:
        condense_question_llm = ChatOpenAI(
            streaming=chat_args.streaming,
            temperature=0
        )

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata
    )

##########################3
def build_chat(chat_args: ChatArgs):
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)

    print("###############################")
    print(f"memoria: {memory_name}, llm: {llm_name}, retriever: {retriever_name}")
    print("###############################")
    
    set_conversation_components(chat_args.conversation_id, llm=llm_name, retriever=retriever_name, memory=memory_name)

    additional_prompt = chat_args.additional_prompt

    # Construimos el mensaje para el LLM sin duplicar la pregunta
    initial_prompt = f"{additional_prompt}\nPregunta del usuario: {chat_args.prompt}"


    condense_question_llm = (
        ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
        if llm_name == "claude-3"
        else ChatOpenAI(streaming=False)  # Asegúrate de establecer la temperatura a 0
    )

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata  
    )
