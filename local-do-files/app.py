"""
Este módulo define una aplicación Flask que permite la carga y descarga de archivos PDF.
Incluye rutas para subir archivos y descargar archivos desde una carpeta de uploads.
"""

from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


app = Flask(__name__)
CORS(app)  # Habilita CORS para la aplicación Flask

UPLOAD_FOLDER = "uploads"  # Define la carpeta de uploads
ALLOWED_EXTENSIONS = {"pdf"}  # Extensiones permitidas para los archivos

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # Configura la carpeta de uploads en la aplicación Flask

def allowed_file(filename):
    """
    Verifica si un archivo tiene una extensión permitida.

    :param filename: Nombre del archivo
    :return: True si la extensión del archivo está permitida, False en caso contrario
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Maneja la subida de archivos.

    :return: Respuesta JSON indicando el estado de la subida
    """
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}, 400)
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}, 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify({"message": f"File {filename} uploaded successfully"}, 200)
    else:
        return jsonify({"message": "File type not allowed"}, 400)

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """
    Maneja la descarga de archivos.

    :param filename: Nombre del archivo a descargar
    :return: El archivo solicitado si existe, de lo contrario un mensaje de error
    """
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=False, mimetype="application/pdf")
    else:
        return jsonify({"message": "File not found"}, 404)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
