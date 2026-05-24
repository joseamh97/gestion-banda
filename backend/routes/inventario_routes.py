from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Inventario, Usuario
from extensions import db

inventario_bp = Blueprint("inventario", __name__)


def get_current_user():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)


def admin_required():
    usuario = get_current_user()
    return usuario and usuario.rol == "admin"


@inventario_bp.route("/", methods=["GET"])
@jwt_required()
def listar_inventario():
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    items = Inventario.query.all()

    return jsonify([i.to_dict() for i in items]), 200


@inventario_bp.route("/", methods=["POST"])
@jwt_required()
def crear_item():
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()

    if not data.get("nombre"):
        return jsonify({"error": "El nombre es obligatorio"}), 400

    if not data.get("categoria"):
        return jsonify({"error": "La categoría es obligatoria"}), 400

    item = Inventario(
        nombre=data.get("nombre"),
        categoria=data.get("categoria"),
        estado=data.get("estado", "disponible"),
        numero_serie=data.get("numero_serie"),
        observaciones=data.get("observaciones"),
        usuario_id=data.get("usuario_id") or None
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "message": "Elemento creado correctamente",
        "item": item.to_dict()
    }), 201


@inventario_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_item(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    item = Inventario.query.get_or_404(id)
    data = request.get_json()

    item.nombre = data.get("nombre", item.nombre)
    item.categoria = data.get("categoria", item.categoria)
    item.estado = data.get("estado", item.estado)
    item.numero_serie = data.get("numero_serie", item.numero_serie)
    item.observaciones = data.get("observaciones", item.observaciones)
    item.usuario_id = data.get("usuario_id") or None

    db.session.commit()

    return jsonify({
        "message": "Elemento actualizado correctamente",
        "item": item.to_dict()
    }), 200


@inventario_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_item(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    item = Inventario.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Elemento eliminado correctamente"
    }), 200