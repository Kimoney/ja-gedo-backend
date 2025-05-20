import pdfplumber
import re 
from flask import Flask, request, jsonify
import os
from sentence_transformers import SentenceTransformer, util
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_section(text, section_titles):
    for title in section_titles:
        pattern = rf"{title}.*?\n(.*?)(\n[A-Z][^\n]+:|\Z)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    return ""

def extract_profile_info(cv_text):
    return {
        "name": re.search(r"(Name|Full Name):?\s*(.*)", cv_text, 
                          re.IGNORECASE).group(2) if re.search(r"(Name|Full Name):?\s*(.*)", cv_text, re.IGNORECASE) else "",
        "email": re.search(r'[\w\.-]+@[\w\.-]+', cv_text).group(0) if re.search(r'[\w\.-]+@[\w\.-]+', cv_text) else "",
        "skills": extract_section(cv_text, ["Skills", "Technical Skills"]),
        "experience": extract_section(cv_text, ["Experience", "Work History"]),
        "tools": extract_section(cv_text, ["Tools", "Equipment"])
    }

def auto_fill_form(profile, form_fields, threshold=0.8):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    keys = list(profile.keys())
    profile_texts = list(profile.values())
    profile_embeddings = model.encode(profile_texts, convert_to_tensor=True)

    auto_filled = {}
    for field_name, field_prompt in form_fields.items():
        field_embedding = model.encode(field_prompt, convert_to_tensor=True)
        sims = util.cos_sim(field_embedding, profile_embeddings)[0]
        best_idx = sims.argmax().item()
        if sims[best_idx] > threshold:
            auto_filled[field_name] = profile[keys[best_idx]]
        else:
            auto_filled[field_name] = ""
    return auto_filled
