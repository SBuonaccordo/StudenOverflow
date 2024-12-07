from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

#Creamos la instancia de la base de datos
db = SQLAlchemy()

jwt = JWTManager()