from datetime import datetime
from app.extensions import db

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
    pregunta = db.relationship('Pregunta', backref=db.backref('respuestas', lazy=True))

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('User', backref=db.backref('respuestas', lazy=True))

    def __init__(self, contenido, id_pregunta, id_usuario):
        self.contenido = contenido
        self.id_pregunta = id_pregunta
        self.id_usuario = id_usuario