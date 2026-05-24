from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Usuario
from extensions import db

user_bp = Blueprint("usuarios", __name__)


def get_current_user():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)


def admin_required():
    usuario = get_current_user()
    return usuario and usuario.rol == "admin"


@user_bp.route("/", methods=["GET"])
@jwt_required()
def listar_usuarios():
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200


@user_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def obtener_usuario(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    usuario = Usuario.query.get_or_404(id)
    return jsonify(usuario.to_dict()), 200


@user_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_usuario(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    usuario = Usuario.query.get_or_404(id)
    data = request.get_json()
    if data.get("rol") and data["rol"] not in ["admin", "musico"]:
        return jsonify({"error": "Rol no válido"}), 400

    if data.get("rol") == "musico":
        if not data.get("instrumento"):
            return jsonify({
                "error": "El instrumento es obligatorio para músicos"
            }), 400

        if not data.get("voz"):
            return jsonify({
                "error": "La voz es obligatoria para músicos"
            }), 400
        
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.apellidos = data.get("apellidos", usuario.apellidos)
    usuario.email = data.get("email", usuario.email)
    usuario.rol = data.get("rol", usuario.rol)
    usuario.instrumento = data.get("instrumento", usuario.instrumento)
    usuario.voz = data.get("voz", usuario.voz)
    usuario.telefono = data.get("telefono", usuario.telefono)
    usuario.activo = data.get("activo", usuario.activo)

    if data.get("password"):
        usuario.set_password(data["password"])

    db.session.commit()

    return jsonify({
        "message": "Usuario actualizado correctamente",
        "usuario": usuario.to_dict()
    }), 200


@user_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario(id):
    if not admin_required():
        return jsonify({"error": "No autorizado"}), 403

    usuario = Usuario.query.get_or_404(id)
    usuario.activo = False
    db.session.commit()

    return jsonify({"message": "Usuario dado de baja correctamente"}), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def actualizar_mi_perfil():

    usuario_id = get_jwt_identity()

    usuario = Usuario.query.get_or_404(usuario_id)

    data = request.get_json()

    usuario.nombre = data.get(
        "nombre",
        usuario.nombre
    )

    usuario.apellidos = data.get(
        "apellidos",
        usuario.apellidos
    )

    usuario.email = data.get(
        "email",
        usuario.email
    )

    usuario.telefono = data.get(
        "telefono",
        usuario.telefono
    )

    if data.get("password"):
        usuario.set_password(data["password"])

    db.session.commit()

    return jsonify({
        "message": "Perfil actualizado",
        "usuario": usuario.to_dict()
    }), 200