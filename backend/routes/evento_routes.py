from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Evento, Usuario, Asistencia
from extensions import db

from datetime import datetime

evento_bp = Blueprint("eventos", __name__)


def get_current_user():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)


def admin_required():
    usuario = get_current_user()
    return usuario and usuario.rol == "admin"


@evento_bp.route("/", methods=["GET"])
@jwt_required()
def listar_eventos():

    usuario = get_current_user()

    eventos = Evento.query.order_by(
        Evento.fecha.asc()
    ).all()

    resultado = []

    for evento in eventos:

        evento_dict = evento.to_dict()

        if usuario.rol == "musico":

            asistencia = Asistencia.query.filter_by(
                evento_id=evento.id,
                usuario_id=usuario.id
            ).first()

            if asistencia:
                evento_dict["mi_asistencia"] = {
                    "estado": asistencia.estado,
                    "comentario": asistencia.comentario
                }
            else:
                evento_dict["mi_asistencia"] = None

        resultado.append(evento_dict)

    return jsonify(resultado), 200


@evento_bp.route("/", methods=["POST"])
@jwt_required()
def crear_evento():

    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()

    required = ["titulo", "tipo", "fecha", "hora"]

    for field in required:
        if not data.get(field):
            return jsonify({
                "error": f"El campo {field} es obligatorio"
            }), 400

    if data["tipo"] not in ["ensayo", "concierto", "procesion"]:
        return jsonify({
            "error": "Tipo de evento no válido"
        }), 400

    evento = Evento(
        titulo=data["titulo"],
        tipo=data["tipo"],
        descripcion=data.get("descripcion"),
        fecha=datetime.strptime(
            data["fecha"],
            "%Y-%m-%d"
        ).date(),
        hora=datetime.strptime(
            data["hora"],
            "%H:%M"
        ).time(),
        ubicacion=data.get("ubicacion")
    )

    db.session.add(evento)
    db.session.commit()

    return jsonify({
        "message": "Evento creado correctamente",
        "evento": evento.to_dict()
    }), 201


@evento_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def obtener_evento(id):

    evento = Evento.query.get_or_404(id)

    return jsonify(evento.to_dict()), 200


@evento_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_evento(id):

    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    evento = Evento.query.get_or_404(id)

    data = request.get_json()

    if data.get("tipo") and data["tipo"] not in ["ensayo", "concierto", "procesion"]:
        return jsonify({
        "error": "Tipo de evento no válido"
    }), 400

    if data.get("titulo"):
        evento.titulo = data["titulo"]

    if data.get("tipo"):
        evento.tipo = data["tipo"]

    if data.get("descripcion"):
        evento.descripcion = data["descripcion"]

    if data.get("fecha"):
        evento.fecha = datetime.strptime(
            data["fecha"],
            "%Y-%m-%d"
        ).date()

    if data.get("hora"):
        evento.hora = datetime.strptime(
            data["hora"],
            "%H:%M"
        ).time()

    if data.get("ubicacion"):
        evento.ubicacion = data["ubicacion"]

    db.session.commit()

    return jsonify({
        "message": "Evento actualizado correctamente",
        "evento": evento.to_dict()
    }), 200


@evento_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_evento(id):

    from models import Asistencia

    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    evento = Evento.query.get_or_404(id)

    Asistencia.query.filter_by(
        evento_id=id
    ).delete(synchronize_session=False)

    db.session.delete(evento)

    db.session.commit()

    return jsonify({
        "message": "Evento eliminado correctamente"
    }), 200