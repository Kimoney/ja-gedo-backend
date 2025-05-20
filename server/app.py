# from flask import Flask
# from flask_cors import CORS
# from flask_migrate import Migrate
# from .models import db
# from .config import Config
# import os

# def create_app():
#     app = Flask(__name__)
    
#     app.secret_key = Config.SECRET_KEY
#     CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://ja-gedo-frontend.vercel.app/"], "supports_credentials": True}})

#     # SQLite database path
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     sqlite_path = os.path.join(basedir, 'app.db')
#     app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{sqlite_path}"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate = Migrate(app, db)

#     with app.app_context():
#         from .routes import main
#         from .routes import ai_chatbot_bp
#         from .routes import upload_cv_bp
#         from .routes import auto_fill_bp
#         from .routes import match_bp 

#         API_PREFIX = '/api/v1'

#         app.register_blueprint(main, url_prefix = API_PREFIX) 
#         app.register_blueprint(ai_chatbot_bp, url_prefix=f'{API_PREFIX}/chatbot') 
#         app.register_blueprint(upload_cv_bp, url_prefix=f'{API_PREFIX}/upload-cv') 
#         app.register_blueprint(auto_fill_bp, url_prefix=f'{API_PREFIX}/auto-fill') 
#         app.register_blueprint(match_bp, url_prefix=API_PREFIX) 

        
#         print("Registered Routes:")
#         for rule in app.url_map.iter_rules():
#             print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, Path: {rule.rule}")

#     return app


