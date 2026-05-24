from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models import Usuario, Obra, Evento, Particella, Asistencia, Inventario

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/stats", methods=["GET"])
@jwt_required()
def obtener_stats():

    total_usuarios = Usuario.query.count()
    usuarios_activos = Usuario.query.filter_by(
        activo=True
    ).count()

    usuarios_inactivos = Usuario.query.filter_by(
        activo=False
    ).count()

    total_eventos = Evento.query.count()

    total_ensayos = Evento.query.filter_by(
        tipo="ensayo"
    ).count()

    total_conciertos = Evento.query.filter_by(
        tipo="concierto"
    ).count()

    total_procesiones = Evento.query.filter_by(
        tipo="procesion"
    ).count()

    total_asistencias = Asistencia.query.count()

    total_asistiran = Asistencia.query.filter_by(
        estado="asistira"
    ).count()

    total_no_asistiran = Asistencia.query.filter_by(
        estado="no_asistira"
    ).count()

    if total_asistencias > 0:
        porcentaje_asistencia = round(
            (total_asistiran / total_asistencias) * 100,
            2
        )
    else:
        porcentaje_asistencia = 0

    total_inventario = Inventario.query.count()

    inventario_disponible = Inventario.query.filter_by(
        estado="disponible"
    ).count()

    inventario_prestado = Inventario.query.filter_by(
        estado="prestado"
    ).count()

    inventario_reparacion = Inventario.query.filter_by(
        estado="reparacion"
    ).count()

    inventario_baja = Inventario.query.filter_by(
        estado="baja"
    ).count()

    stats = {

        "usuarios": total_usuarios,
        "usuarios_activos": usuarios_activos,
        "usuarios_inactivos": usuarios_inactivos,

        "obras": Obra.query.count(),
        "particellas": Particella.query.count(),

        "eventos": total_eventos,
        "ensayos": total_ensayos,
        "conciertos": total_conciertos,
        "procesiones": total_procesiones,

        "asistencias": total_asistencias,
        "asistiran": total_asistiran,
        "no_asistiran": total_no_asistiran,
        "porcentaje_asistencia": porcentaje_asistencia,

        "inventario": total_inventario,
        "inventario_disponible": inventario_disponible,
        "inventario_prestado": inventario_prestado,
        "inventario_reparacion": inventario_reparacion,
        "inventario_baja": inventario_baja
    }

    return jsonify(stats), 200