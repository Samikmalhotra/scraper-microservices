from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import redis
from app.RedisClientSingleton import RedisClientSingleton

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    RedisClientSingleton.init_instance()

    from app import routes
    app.register_blueprint(routes.bp)

    return app