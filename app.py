from flask import Flask, request, jsonify
from flask_cors import CORS # Import the Flask-CORS extension
from transformers import pipeline
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) # Enable CORS for all routes and origins

# Configure the upload directory
UPLOAD_FOLDER = 'uploads/beans'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists at startup
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the disease detection pipeline (only once at startup)
try:
    disease_detector = pipeline("image-classification", model="dzinampini/beans-leaf-disease-detection")
    model_loaded = True
except Exception as e:
    disease_detector = None
    model_loaded = False
    model_load_error = str(e)

EXPECTED_API_KEY = "cv001"

def predict_disease(image_path):
    try:
        result = disease_detector(image_path)
        return {"label": result[0]['label'], "score": result[0]['score']}
    except Exception as e:
        return {"error": str(e)}

@app.route('/beans', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"success": False, "result": "No image part in the request"}), 400
    image_path = request.files['image']
    api_key = request.form.get('api_key')
    
    if not api_key:
        return jsonify({"success": False, "result": "Missing 'api_key' in request"}), 401

    if api_key != EXPECTED_API_KEY:
        return jsonify({"success": False, "result": "Invalid API key"}), 401

    filename = secure_filename(image_path.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_path.save(filepath)

    if not image_path:
        return jsonify({"success": False, "result": "Missing 'image_path' in request"}), 400
    
    if not model_loaded:
        return jsonify({"success": False, "result": f"Model loading failed: {model_load_error}"}), 500
    
    # print(filepath)

    # Check if the image path is valid (you might want more robust validation)
    if not os.path.exists(filepath):
        return jsonify({"success": False, "result": f"Image not found at path: {image_path}"}), 400
    
    prediction_result = predict_disease(filepath)

    if "error" in prediction_result:
        return jsonify({"success": False, "result": f"Prediction error: {prediction_result['error']}"}), 500
    else:
        return jsonify({"success": True, "result": prediction_result}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)