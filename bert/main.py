from flask import Flask, request, jsonify, render_template_string
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Load the model and tokenizer
model_name = "nlpaueb/legal-bert-base-uncased"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    # Get the label mappings
    id2label = model.config.id2label
    label2id = model.config.label2id
    num_labels = len(id2label)
    logging.info(f"Model loaded successfully. Number of labels: {num_labels}")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    model = None
    tokenizer = None
    id2label = {}
    label2id = {}

# Read the HTML content
try:
    with open('index.html', 'r') as file:
        html_content = file.read()
except FileNotFoundError:
    html_content = "<h1>Error: index.html not found</h1>"

@app.route('/')
def home():
    return render_template_string(html_content)

@app.route('/classify', methods=['POST'])
def classify():
    if model is None or tokenizer is None:
        return jsonify({"error": "Model not loaded properly"}), 500

    payload = request.json
    input_text = payload['inputs']
    
    try:
        # Tokenize and prepare the input
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
        
        # Get prediction
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
        
        # Get the top predictions (up to 3, but not more than the number of labels)
        top_k = min(3, num_labels)
        top_predictions = torch.topk(probabilities, top_k)
        
        # Format the output
        results = [
            {
                "label": id2label[prediction.item()],
                "score": score.item()
            }
            for prediction, score in zip(top_predictions.indices[0], top_predictions.values[0])
        ]
        
        logging.info(f"Classification results: {results}")
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error during classification: {str(e)}")
        return jsonify({"error": f"Classification error: {str(e)}"}), 500

port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)