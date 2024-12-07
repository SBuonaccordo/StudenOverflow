from app.extensions import db
from .usuarios import User

class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship(User, backref='preguntas')
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_actualizacion = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())