from flask import Flask
from flask_restful import Api
from .routes import APIRoutes

from .config import Config
from .extensions import db, jwt

from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import jsonify

def configure_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    
    rutas = APIRoutes()
    rutas.init_api(api)

    @app.errorhandler(NoAuthorizationError)
    def manejar_no_tiken(error):
        return jsonify({
            'Mensaje' : 'Necesitas un token para acceder',
            'Error' : str(error)
        }, 401)
    
    @app.errorhandler(InvalidHeaderError)
    def manejar_token_invalido(error):
        return jsonify({
            'Mensaje' : 'Token invalido o mal formado',
            'Error' : str(error)
        }, 422)
    
    @jwt.expired_token_loader
    def manejar_token_expirado(jwt_header, jwt_payload):
        return jsonify ({
            'Mensaje' : 'El token ya expiró',
            'Error' : 'token expirado'
        })

    return app