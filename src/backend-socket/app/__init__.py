import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
import os

# initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode='eventlet',
    path='/socket'
)

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    else:
        # default config
        from .config import Config
        app.config.from_object(Config)
    
    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    # use redis as message queue
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])
    
    from app import events
    
    return app