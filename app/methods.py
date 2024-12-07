from .models.usuarios import User
from flask import session
from flask_jwt_extended import create_access_token
from datetime import timedelta

from .models.usuarios import User


def user_register(nombre, email, password):
    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente is not None:
        return {'Error': 'El usuario ya está registrado'}, 403
    
    nuevo_usuario = User(nombre=nombre, email=email, password=password)
    nuevo_usuario.hashear_password(password=password)
    nuevo_usuario.save()

    return {
        'Status' : 'Usuario Registrado',
        'Nombre' : nombre,
        'Email' : email
    },200

def user_login(email, password):
    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente is None:
        return {'Status' : 'El correo o la contraseña es incorrecto'}, 400
    
    if usuario_existente.verificar_password(password = password):
        caducidad = timedelta(hours=4)
        token_acceso = create_access_token(identity=usuario_existente.nombre, expires_delta=caducidad)

        session['user_id'] = usuario_existente.id
        session['user_name'] = usuario_existente.nombre

        
        return {
            'Status' : 'Sesión iniciada',
            'Token' : token_acceso
        }
    else:
        return 'Contraseña o usuario incorrecto'

