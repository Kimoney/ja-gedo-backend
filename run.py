# run.py
import sys
from dotenv import load_dotenv
from server.app import create_app 
from flask import Flask
import os


UPLOAD_FOLDER = "uploads"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

sys.path.append('.')

load_dotenv()


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5555))
    app.run(host="0.0.0.0", port=port, debug=True)
