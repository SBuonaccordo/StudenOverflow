from app.extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def hashear_password(self, password):
        self.password = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

