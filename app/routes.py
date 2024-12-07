from flask_restful import Resource 
from flask import request, redirect, session, url_for, render_template, make_response, jsonify

from .methods import user_register, user_login
from .models.usuarios import User, db
from .models.preguntas import Pregunta
from .models.respuestas import Respuesta

from flask_jwt_extended import jwt_required


class Index(Resource):
    def get(self):
        #Renderizar el archivo index.html
        pagina = render_template('index.html')

        #Crear la respuesta con el archivo ya renderizado
        respuesta = make_response(pagina)

        return respuesta
    
class SingUp(Resource):
    def get(self):
        pagina = render_template('singup.html')
        respuesta = make_response(pagina)
        return  respuesta
    
    def post(self):
        user_info = request.form

        nombre = user_info.get('nombre')
        email = user_info.get('email')
        password = user_info.get('password')

        user_register(nombre, email, password)
        
        return redirect(url_for('login'))
    
class Login(Resource):
    def get(self):
        pagina = render_template('login.html')
        respuesta = make_response(pagina)
        return respuesta
    
    def post(self):
        user_inf = request.form

        email = user_inf.get('email')
        password = user_inf.get('password')

        user_login(email, password)

        return redirect(url_for('mostrar_preguntas'))
    
class Restringido(Resource):
    @jwt_required()
    def get(self):
        return {'Mensaje' : 'Estás Loggeado'}
    
class Dashboard(Resource):
    def get(self):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        usuario = User.query.get(user_id)
        
        preguntas_usuario = Pregunta.query.filter_by(id_usuario=user_id).all()

        pagina = render_template('dashboard.html', usuario=usuario, preguntas=preguntas_usuario)
        respuesta = make_response(pagina)
        
        return respuesta
    
class NuevaPreguntas(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        
        pagina = render_template('preguntas.html')
        respuesta = make_response(pagina)
        return respuesta
    
    def post(self):
        id_usuario = session.get('user_id')

        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')

        if not titulo or not contenido:
            return {"mensaje" : "El título y contenido son requeridos"}, 400
        
        nueva_pregunta = Pregunta(titulo=titulo, contenido=contenido, id_usuario=id_usuario)
        db.session.add(nueva_pregunta)
        db.session.commit()

        return jsonify(mensaje="Pregunta creada exitosamente"), redirect(url_for('mostrar_preguntas'))
    
class EliminarPregunta(Resource):
    def post(self, pregunta_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        pregunta = Pregunta.query.get_or_404(pregunta_id)

        if pregunta.id_usuario != user_id:
            return "No tienes permiso para eliminar esta pregunta.", 403
        
        db.session.delete(pregunta)
        db.session.commit()

        return redirect(url_for('dashboard'))
   
class MostrarPreguntas(Resource):
    def get(self):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        usuario = User.query.get(user_id)

        preguntas = Pregunta.query.order_by(Pregunta.fecha_creacion.desc()).all()

        pagina = render_template('preguntas.html', usuario=usuario, preguntas=preguntas)
        respuesta = make_response(pagina)

        return respuesta
    
class ResponderPregunta(Resource):
    def post(self, pregunta_id):
        pregunta = Pregunta.query.get_or_404(pregunta_id)

        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        contenido = request.form.get('contenido')
        if not contenido:
            return redirect(url_for('preguntas'))

        respuesta = Respuesta(contenido=contenido, id_pregunta=pregunta_id, id_usuario=session['user_id'])
        db.session.add(respuesta)
        db.session.commit()

        return redirect(url_for('mostrar_preguntas'))

class EditarRespusta(Resource):
    def post(self, respuesta_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        respuesta = Respuesta.query.get_or_404(respuesta_id)

        if respuesta.id_usuario != session['user_id']:
            return "No tienes permiso para editar esta respuesta", 403
        
        contenido = request.form.get('contenido')
        if not contenido:
            return "El contenido no puede estar vacio", 400
        
        respuesta.contenido = contenido
        db.session.commit()

        return redirect(url_for('mostrar_preguntas'))
    
class EliminarRespuesta(Resource):
    def post(self, respuesta_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        respuesta = Respuesta.query.get_or_404(respuesta_id)

        if respuesta.id_usuario != user_id:
            return "No tienes permiso para eliminar esta respuesta.", 403
        
        db.session.delete(respuesta)
        db.session.commit()

        return redirect(url_for('mostrar_preguntas'))
    
class Logout(Resource):
    def get(self):
        session.clear()
        return 'Sesión cerrada exitosamente', redirect(url_for('login'))


class APIRoutes:
    def init_api(self, api):
        api.add_resource(Index, '/')
        api.add_resource(SingUp, '/singup')
        api.add_resource(Login, '/login')
        api.add_resource(Restringido, '/restringido')
        api.add_resource(Dashboard, '/dashboard')
        api.add_resource(NuevaPreguntas, '/pregunta', endpoint='nueva_pregunta')
        api.add_resource(EliminarPregunta, '/preguntas/<int:pregunta_id>/eliminar', endpoint='eliminar_pregunta')
        api.add_resource(MostrarPreguntas, '/preguntas', endpoint='mostrar_preguntas')
        api.add_resource(ResponderPregunta, '/preguntas/<int:pregunta_id>/responder', endpoint='responder_pregunta')
        api.add_resource(EditarRespusta, '/respuestas/<int:respuesta_id>/editar', endpoint='editar_respuesta')
        api.add_resource(EliminarRespuesta, '/respuestas/<int:respuesta_id>/eliminar', endpoint='eliminar_respuesta')
        api.add_resource(Logout, '/logout')
