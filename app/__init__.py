from flask import Flask
from flask_bootstrap import Bootstrap  
from flask_login import LoginManager
from flask_mysqldb import MySQL
from .config import Config


bootstrap = Bootstrap()
mysql = MySQL()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    bootstrap.init_app(app)
    mysql.init_app(app)
    login_manager.init_app(app)
    
    
    from .views import main, auth, products
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(products)
    
    
    from .errors import register_error_handlers
    register_error_handlers(app)
    
    return app