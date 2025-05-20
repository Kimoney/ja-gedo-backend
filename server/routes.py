from flask import Blueprint, request, jsonify
from flask_restful import Api
import sys
from dotenv import load_dotenv
from server.app import create_app 
import os
from werkzeug.utils import secure_filename
from server.cv_parser import allowed_file, extract_profile_info, extract_text_from_pdf, auto_fill_form 
from server.chatbot import ask_ai_agent
from server.cv_parser import extract_text_from_pdf, extract_profile_info
from server.cv_parser import auto_fill_form
from sentence_transformers import SentenceTransformer, util
import json

main = Blueprint('main', __name__)
api = Api(main)

# API Version 1 Prefix
API_PREFIX = '/api/v1'

@main.route('/')
def home():
    return 'Welcome To Ja Gedo API!'


ai_chatbot_bp = Blueprint("chatbot", __name__)

@ai_chatbot_bp.route("/chatbot", methods=["POST"])
def handle_ai_chatbot():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    question = data["message"]
    response = ask_ai_agent(question)
    return jsonify({"response": response}) 


upload_cv_bp = Blueprint("upload_cv", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_cv_bp.route("/upload-cv", methods=["POST"])
def upload_cv():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        return jsonify({"message": "CV uploaded successfully", "filename": filename}), 200

    return jsonify({"error": "Invalid file type. Only PDF allowed."}), 400



auto_fill_bp = Blueprint("auto_fill", __name__)

@auto_fill_bp.route("/auto-fill", methods=["POST"])
def handle_auto_fill():
    file = request.files.get("cv")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_path = f"app/static/uploads/{file.filename}"
    file.save(file_path)

    text = extract_text_from_pdf(file_path)
    profile = extract_profile_info(text)

    form_fields = {
        "full_name": "Enter your full name",
        "contact_email": "Your email address",
        "relevant_experience": "Briefly describe your experience with similar projects",
        "tools_available": "List any tools or equipment you will bring to the job",
        "skills_required": "Mention the skills you will use for this project"
    }

    filled = auto_fill_form(profile, form_fields)
    return jsonify({"auto_filled": filled})



match_bp = Blueprint("match_maker", __name__)
model = SentenceTransformer("all-MiniLM-L6-v2") 

@match_bp.route("/api/match", methods=["POST"])
def match_profiles():
    data = request.get_json()

    if not data or "project_description" not in data or "fundis" not in data:
        return jsonify({"error": "Missing 'project_description' or 'fundis' in request"}), 400

    project_desc = data["project_description"]
    fundis = data["fundis"]  

    if not isinstance(fundis, list):
        return jsonify({"error": "'fundis' must be a list"}), 400

    project_embedding = model.encode(project_desc, convert_to_tensor=True)

    scored_fundis = []
    for fundi in fundis:
        fundi_id = fundi.get("id")
        profile_text = fundi.get("profile", "")

        profile_embedding = model.encode(profile_text, convert_to_tensor=True)
        similarity = util.cos_sim(project_embedding, profile_embedding).item()

        scored_fundis.append({
            "id": fundi_id,
            "similarity": round(similarity, 4)
        })

    scored_fundis.sort(key=lambda x: x["similarity"], reverse=True)

    return jsonify({"matches": scored_fundis})





