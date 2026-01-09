from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev_key'

    from .auth import auth
    from .main import main
    from .admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    
    return app