# from flask import Blueprint, g, jsonify
# from werkzeug.exceptions import Unauthorized
# from app.web.hooks import login_required, handle_file_upload, load_model
# from app.web.db.models import Pdf
# from app.web.tasks.embeddings import process_document
# from app.web import files
# from flask import Blueprint, g, jsonify
# from app.web.hooks import login_required
# from app.web.db.models import Pdf


# bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")

# # @bp.route("/", methods=["GET"])
# # @login_required
# # def list():
# #     pdfs = Pdf.where(user_id=g.user.id)
# #     pdf_ids = [pdf.id for pdf in pdfs]
# #     return jsonify(pdf_ids)


# @bp.route("/", methods=["GET"])
# @login_required
# def list():
#     pdfs = Pdf.where(user_id=g.user.id)

#     return Pdf.as_dicts(pdfs)


# @bp.route("/", methods=["POST"])
# @login_required
# @handle_file_upload
# def upload_file(file_id, file_path, file_name):
#     res, status_code = files.upload(file_path)
#     if status_code >= 400:
#         return res, status_code

#     pdf = Pdf.create(id=file_id, name=file_name, user_id=g.user.id)

#     process_document.delay(pdf.id)

#     return pdf.as_dict()


# @bp.route("/<string:pdf_id>", methods=["GET"])
# @login_required
# @load_model(Pdf)
# def show(pdf):
#     return jsonify(
#         {
#             "pdf": pdf.as_dict(),
#             "download_url": files.create_download_url(pdf.id),
#         }
#     )



from flask import Blueprint, g, jsonify, request, session
from werkzeug.exceptions import Unauthorized
from app.web.hooks import login_required, handle_file_upload, load_model
from app.web.db.models import Pdf
from app.web.tasks.embeddings import process_document
from app.web import files

bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")

@bp.route("/", methods=["GET"])
@login_required
def list():
    pdfs = Pdf.where(user_id=g.user.id)
    return Pdf.as_dicts(pdfs)

@bp.route("/", methods=["POST"])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name):
    res, status_code = files.upload(file_path)
    if status_code >= 400:
        return res, status_code

    pdf = Pdf.create(id=file_id, name=file_name, user_id=g.user.id)
    process_document.delay(pdf.id)
    return pdf.as_dict()

@bp.route("/<string:pdf_id>", methods=["GET"])
@login_required
@load_model(Pdf)
def show(pdf):
    return jsonify({
        "pdf": pdf.as_dict(),
        "download_url": files.create_download_url(pdf.id),
    })

@bp.route("/selected-pdfs", methods=["POST"], endpoint='pdf_selected_pdfs')
@login_required
def selected_pdfs():
    data = request.get_json()
    pdf_ids = data.get('pdf_ids', [])
    print(f"Received PDF IDs: {pdf_ids}")  # Aquí para verificar las IDs recibidas
    session['selected_pdfs'] = pdf_ids  # Guardar en la sesión del usuario
    return jsonify({"message": "PDF IDs recibidos", "pdf_ids": pdf_ids})

def get_selected_pdfs():
    return session.get('selected_pdfs', [])
