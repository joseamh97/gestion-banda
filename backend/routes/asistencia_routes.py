from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Asistencia, Evento, Usuario
from extensions import db

asistencia_bp = Blueprint("asistencias", __name__)


def get_current_user():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)


@asistencia_bp.route("/evento/<int:evento_id>", methods=["GET"])
@jwt_required()
def listar_asistencias(evento_id):

    asistencias = Asistencia.query.filter_by(
        evento_id=evento_id
    ).all()

    return jsonify([
        a.to_dict() for a in asistencias
    ]), 200


@asistencia_bp.route("/", methods=["POST"])
@jwt_required()
def responder_asistencia():

    usuario = get_current_user()

    data = request.get_json()

    evento_id = data.get("evento_id")
    estado = data.get("estado")
    comentario = data.get("comentario")

    if not evento_id or not estado:
        return jsonify({
            "error": "Faltan datos"
        }), 400

    evento = Evento.query.get(evento_id)

    if not evento:
        return jsonify({
            "error": "Evento no encontrado"
        }), 404

    asistencia = Asistencia.query.filter_by(
        usuario_id=usuario.id,
        evento_id=evento_id
    ).first()

    if asistencia:

        asistencia.estado = estado
        asistencia.comentario = comentario

    else:

        asistencia = Asistencia(
            usuario_id=usuario.id,
            evento_id=evento_id,
            estado=estado,
            comentario=comentario
        )

        db.session.add(asistencia)

    db.session.commit()

    return jsonify({
        "message": "Asistencia registrada",
        "asistencia": asistencia.to_dict()
    }), 200