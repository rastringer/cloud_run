import os
import sys
from flask import Flask, render_template, request
import spacy
import requests
from bs4 import BeautifulSoup

# Create the Flask app at the module level
app = Flask(__name__)

# Load spaCy model once when the application starts
print("Loading spaCy model...")
try:
    nlp = spacy.load("en_core_web_lg")
    print("spaCy model loaded successfully.")
except OSError as e:
    print(f"Error loading spaCy model: {e}", file=sys.stderr)
    print("Python executable:", sys.executable, file=sys.stderr)
    print("Python version:", sys.version, file=sys.stderr)
    print("spaCy version:", spacy.__version__, file=sys.stderr)
    print("Current working directory:", os.getcwd(), file=sys.stderr)
    print("Contents of current directory:", os.listdir(), file=sys.stderr)
    raise

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_type = request.form["input_type"]
        input_data = request.form["input_data"]
        
        if input_type == "file":
            # Process uploaded file
            file = request.files["file"]
            if file:
                text = file.read().decode("utf-8")
            else:
                return "No file uploaded", 400
        elif input_type == "url":
            # Fetch and process web page content
            response = requests.get(input_data)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()
        else:
            return "Invalid input type", 400
        
        # Count characters
        char_count = len(text)
        
        # Perform NER
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        return render_template("results.html", entities=entities, char_count=char_count)
    
    return render_template("index.html")

# This block is now outside the if __name__ == "__main__" check
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)