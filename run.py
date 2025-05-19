# run.py
import sys
from dotenv import load_dotenv

sys.path.append('.')

# Load environment variables
load_dotenv()

from server.app import create_app

if __name__ == "__main__":
    import os

    app = create_app()
    port = int(os.environ.get("PORT", 5555))
    app.run(host="0.0.0.0", port=port, debug=True)
