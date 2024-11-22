from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from dotenv import load_dotenv

import threading
from app.RedisClientSingleton import RedisClientSingleton

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # load_dotenv()

    app.config.from_object('app.config.Config')

    RedisClientSingleton.init_instance()

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from app import routes
    app.register_blueprint(routes.bp)

    return app

