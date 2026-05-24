from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import Usuario
from extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required = ["nombre", "apellidos", "email", "password"]
    rol = data.get("rol", "musico")

    if rol not in ["admin", "musico"]:
        return jsonify({"error": "Rol no válido"}), 400

    if rol == "musico":
        if not data.get("instrumento"):
            return jsonify({"error": "El instrumento es obligatorio para músicos"}), 400

        if not data.get("voz"):
            return jsonify({"error": "La voz es obligatoria para músicos"}), 400
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"El campo {field} es obligatorio"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    usuario = Usuario(
        nombre=data["nombre"],
        apellidos=data["apellidos"],
        email=data["email"],
        rol=data.get("rol", "musico"),
        instrumento=data.get("instrumento"),
        voz=data.get("voz"),
        telefono=data.get("telefono")
    )

    usuario.set_password(data["password"])

    db.session.add(usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuario registrado correctamente",
        "usuario": usuario.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    usuario = Usuario.query.filter_by(email=email, activo=True).first()

    if not usuario or not usuario.check_password(password):
        return jsonify({"error": "Credenciales no válidas"}), 401

    token = create_access_token(identity=str(usuario.id))

    return jsonify({
        "access_token": token,
        "usuario": usuario.to_dict()
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario.to_dict()), 200