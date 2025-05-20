from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .models import db
from .config import DbConnection, Config
from server.routes import ai_chatbot_bp

def create_app():
    app = Flask(__name__)
    
    app.secret_key = Config.SECRET_KEY
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://ja-gedo-frontend.vercel.app/"], "supports_credentials": True}})
    
    # Use environment variables to get sensitive information
    db_user = DbConnection.DB_USER
    db_password = DbConnection.DB_PASSWORD
    db_name = DbConnection.DB_NAME
    db_host = DbConnection.DB_HOST
    db_port = DbConnection.DB_PORT 

    # Configure the application
    
    # PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    app.register_blueprint(ai_chatbot_bp)

    # Register blueprints or routes
    with app.app_context():
        from .routes import main 
        from .routes import ai_chatbot_bp 
        from .routes import upload_cv_bp
        from .routes import auto_fill_bp
        from .routes import match_bp
        app.register_blueprint(main, ai_chatbot_bp, upload_cv_bp, auto_fill_bp, match_bp) 

    return app 