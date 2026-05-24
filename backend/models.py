from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    rol = db.Column(db.String(50), nullable=False, default="musico")
    instrumento = db.Column(db.String(100), nullable=True)
    voz = db.Column(db.String(50), nullable=True)

    telefono = db.Column(db.String(20), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "rol": self.rol,
            "instrumento": self.instrumento,
            "voz": self.voz,
            "telefono": self.telefono,
            "activo": self.activo
        }


class Obra(db.Model):
    __tablename__ = "obras"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    compositor = db.Column(db.String(150), nullable=True)
    genero = db.Column(db.String(100), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)

    particellas = db.relationship(
        "Particella",
        backref="obra",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "compositor": self.compositor,
            "genero": self.genero,
            "descripcion": self.descripcion
        }


class Particella(db.Model):
    __tablename__ = "particellas"

    id = db.Column(db.Integer, primary_key=True)
    obra_id = db.Column(db.Integer, db.ForeignKey("obras.id"), nullable=False)

    instrumento = db.Column(db.String(100), nullable=False)
    voz = db.Column(db.String(50), nullable=False)

    archivo_pdf = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "obra_id": self.obra_id,
            "obra": self.obra.titulo if self.obra else None,
            "instrumento": self.instrumento,
            "voz": self.voz,
            "archivo_pdf": self.archivo_pdf
        }

class Evento(db.Model):
    __tablename__ = "eventos"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)
    # ensayo / concierto / procesion

    descripcion = db.Column(db.Text)

    fecha = db.Column(db.Date, nullable=False)

    hora = db.Column(db.Time, nullable=False)

    ubicacion = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "fecha": self.fecha.strftime("%Y-%m-%d"),
            "hora": self.hora.strftime("%H:%M"),
            "ubicacion": self.ubicacion
        }
    

class Asistencia(db.Model):
    __tablename__ = "asistencias"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("eventos.id"),
        nullable=False
    )

    estado = db.Column(
        db.String(20),
        nullable=False,
        default="pendiente"
    )
    # asistira / no_asistira / pendiente

    comentario = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario = db.relationship("Usuario")
    evento = db.relationship("Evento")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "evento_id": self.evento_id,
            "estado": self.estado,
            "comentario": self.comentario,
            "usuario": f"{self.usuario.nombre} {self.usuario.apellidos}",
            "evento": self.evento.titulo
        }    
    
class Inventario(db.Model):
    __tablename__ = "inventario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default="disponible")
    numero_serie = db.Column(db.String(100), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)

    usuario = db.relationship("Usuario", backref="material_asignado")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "estado": self.estado,
            "numero_serie": self.numero_serie,
            "observaciones": self.observaciones,
            "usuario_id": self.usuario_id,
            "usuario": self.usuario.nombre if self.usuario else None
        }