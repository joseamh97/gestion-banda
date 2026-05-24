from flask import Flask, send_from_directory
from config import Config
from extensions import db, migrate, jwt, cors

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.obra_routes import obra_bp
from routes.particella_routes import particella_bp
from routes.evento_routes import evento_bp
from routes.asistencia_routes import asistencia_bp
from routes.dashboard_routes import dashboard_bp
from routes.inventario_routes import inventario_bp
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/usuarios")
    app.register_blueprint(obra_bp, url_prefix="/api/obras")
    app.register_blueprint(particella_bp, url_prefix="/api/particellas")
    app.register_blueprint(evento_bp, url_prefix="/api/eventos")
    app.register_blueprint(asistencia_bp, url_prefix="/api/asistencias")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(inventario_bp, url_prefix="/api/inventario")

    @app.route("/")
    def index():
        return {"message": "API gestión de bandas funcionando"}

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory("uploads", filename)
    
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)