from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Obra, Usuario
from extensions import db

obra_bp = Blueprint("obras", __name__)


def get_current_user():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)


def admin_required():
    usuario = get_current_user()
    return usuario and usuario.rol == "admin"


@obra_bp.route("/", methods=["GET"])
@jwt_required()
def listar_obras():
    obras = Obra.query.all()
    return jsonify([obra.to_dict() for obra in obras]), 200


@obra_bp.route("/", methods=["POST"])
@jwt_required()
def crear_obra():
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()

    if not data.get("titulo"):
        return jsonify({"error": "El título es obligatorio"}), 400

    obra = Obra(
        titulo=data["titulo"],
        compositor=data.get("compositor"),
        genero=data.get("genero"),
        descripcion=data.get("descripcion")
    )

    db.session.add(obra)
    db.session.commit()

    return jsonify({
        "message": "Obra creada correctamente",
        "obra": obra.to_dict()
    }), 201


@obra_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def obtener_obra(id):
    obra = Obra.query.get_or_404(id)
    return jsonify(obra.to_dict()), 200


@obra_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_obra(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    obra = Obra.query.get_or_404(id)
    data = request.get_json()

    obra.titulo = data.get("titulo", obra.titulo)
    obra.compositor = data.get("compositor", obra.compositor)
    obra.genero = data.get("genero", obra.genero)
    obra.descripcion = data.get("descripcion", obra.descripcion)

    db.session.commit()

    return jsonify({
        "message": "Obra actualizada correctamente",
        "obra": obra.to_dict()
    }), 200


@obra_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_obra(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    obra = Obra.query.get_or_404(id)

    db.session.delete(obra)
    db.session.commit()

    return jsonify({"message": "Obra eliminada correctamente"}), 200