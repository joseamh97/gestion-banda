import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from models import Particella, Usuario, Obra
from extensions import db

particella_bp = Blueprint("particellas", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}


def get_current_user():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)


def admin_required():
    usuario = get_current_user()
    return usuario and usuario.rol == "admin"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@particella_bp.route("/", methods=["GET"])
@jwt_required()
def listar_particellas():
    usuario = get_current_user()

    if usuario.rol == "admin":
        particellas = Particella.query.all()
    else:
        particellas = Particella.query.filter_by(
            instrumento=usuario.instrumento,
            voz=usuario.voz
        ).all()

    return jsonify([p.to_dict() for p in particellas]), 200


@particella_bp.route("/mis-particellas", methods=["GET"])
@jwt_required()
def mis_particellas():
    usuario = get_current_user()

    particellas = Particella.query.filter_by(
        instrumento=usuario.instrumento,
        voz=usuario.voz
    ).all()

    return jsonify([p.to_dict() for p in particellas]), 200


@particella_bp.route("/", methods=["POST"])
@jwt_required()
def crear_particella():
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    obra_id = request.form.get("obra_id")
    instrumento = request.form.get("instrumento") or "Pendiente"
    voz = request.form.get("voz") or "Pendiente"
    archivos = request.files.getlist("archivo_pdf")

    if not obra_id:
        return jsonify({"error": "La obra es obligatoria"}), 400

    if not archivos:
        return jsonify({"error": "Debes seleccionar al menos un PDF"}), 400

    obra = Obra.query.get(obra_id)

    if not obra:
        return jsonify({"error": "La obra no existe"}), 404

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    particellas_creadas = []

    for archivo in archivos:
        if not archivo or archivo.filename == "":
            continue

        if not allowed_file(archivo.filename):
            return jsonify({"error": "Solo se permiten archivos PDF"}), 400

        filename = secure_filename(
            f"obra_{obra_id}_{instrumento}_{voz}_{archivo.filename}"
        )

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(file_path)

        particella = Particella(
            obra_id=obra_id,
            instrumento=instrumento,
            voz=voz,
            archivo_pdf=file_path.replace("\\", "/")
        )

        db.session.add(particella)
        particellas_creadas.append(particella)

    if len(particellas_creadas) == 0:
        return jsonify({"error": "No se ha recibido ningún PDF válido"}), 400

    db.session.commit()

    return jsonify({
        "message": "Particellas creadas correctamente",
        "particellas": [p.to_dict() for p in particellas_creadas]
    }), 201


@particella_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def obtener_particella(id):
    usuario = get_current_user()
    particella = Particella.query.get_or_404(id)

    if usuario.rol != "admin":
        if (
            particella.instrumento != usuario.instrumento
            or particella.voz != usuario.voz
        ):
            return jsonify({"error": "No tienes acceso a esta particella"}), 403

    return jsonify(particella.to_dict()), 200


@particella_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_particella(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    particella = Particella.query.get_or_404(id)

    obra_id = request.form.get("obra_id")
    instrumento = request.form.get("instrumento")
    voz = request.form.get("voz")
    archivo = request.files.get("archivo_pdf")

    if obra_id:
        obra = Obra.query.get(obra_id)

        if not obra:
            return jsonify({"error": "La obra no existe"}), 404

        particella.obra_id = obra_id

    if instrumento is not None:
        if instrumento.strip() == "":
            return jsonify({"error": "El instrumento no puede estar vacío"}), 400

        particella.instrumento = instrumento

    if voz is not None:
        if voz.strip() == "":
            return jsonify({"error": "La voz no puede estar vacía"}), 400

        particella.voz = voz

    if archivo:
        if not allowed_file(archivo.filename):
            return jsonify({"error": "Solo se permiten archivos PDF"}), 400

        if particella.archivo_pdf and os.path.exists(particella.archivo_pdf):
            os.remove(particella.archivo_pdf)

        filename = secure_filename(
            f"obra_{particella.obra_id}_{particella.instrumento}_{particella.voz}_{archivo.filename}"
        )

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        archivo.save(file_path)

        particella.archivo_pdf = file_path.replace("\\", "/")

    db.session.commit()

    return jsonify({
        "message": "Particella actualizada correctamente",
        "particella": particella.to_dict()
    }), 200


@particella_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_particella(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    particella = Particella.query.get_or_404(id)

    if particella.archivo_pdf and os.path.exists(particella.archivo_pdf):
        os.remove(particella.archivo_pdf)

    db.session.delete(particella)
    db.session.commit()

    return jsonify({"message": "Particella eliminada correctamente"}), 200