import os

class Config:
    #Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://so_user:qyhsok-2kuxci-fUmceg@localhost/studentoverflow")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'c39f303627bb5b36ae7f4d3893bbf2bee9463800'
    PROPAGATE_EXCEPTION = True
    SECRET_KEY = os.urandom(24)
    
    
    