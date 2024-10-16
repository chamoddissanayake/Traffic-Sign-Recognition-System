import os
import time
import subprocess
from flask import Flask, request, send_from_directory, jsonify
from keras.models import load_model
import numpy as np
from PIL import Image
from flask_cors import CORS

# Define the classes
classes = { 
    1: 'Speed limit (20km/h)', 2: 'Speed limit (30km/h)', 3: 'Speed limit (50km/h)',
    4: 'Speed limit (60km/h)', 5: 'Speed limit (70km/h)', 6: 'Speed limit (80km/h)',
    7: 'End of speed limit (80km/h)', 8: 'Speed limit (100km/h)', 9: 'Speed limit (120km/h)',
    10: 'No passing', 11: 'No passing veh over 3.5 tons', 12: 'Right-of-way at intersection',
    13: 'Priority road', 14: 'Yield', 15: 'Stop', 16: 'No vehicles', 17: 'Veh > 3.5 tons prohibited',
    18: 'No entry', 19: 'General caution', 20: 'Dangerous curve left', 21: 'Dangerous curve right',
    22: 'Double curve', 23: 'Bumpy road', 24: 'Slippery road', 25: 'Road narrows on the right',
    26: 'Road work', 27: 'Traffic signals', 28: 'Pedestrians', 29: 'Children crossing', 
    30: 'Bicycles crossing', 31: 'Beware of ice/snow', 32: 'Wild animals crossing', 
    33: 'End speed + passing limits', 34: 'Turn right ahead', 35: 'Turn left ahead', 
    36: 'Ahead only', 37: 'Go straight or right', 38: 'Go straight or left', 39: 'Keep right', 
    40: 'Keep left', 41: 'Roundabout mandatory', 42: 'End of no passing', 43: 'End no passing veh > 3.5 tons'
}

app = Flask(__name__)
CORS(app)

# Folder to store uploaded images
UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_image(filename):
    # Use send_from_directory to serve the image file
    return send_from_directory(UPLOAD_FOLDER, filename)

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the model or train if not available
model_path = "../model/traffic_classifier.h5"

def train_model():
    print("Training model...")
    # Run the training script
    subprocess.run(["python", "../train/traffic_sign_train.py"])
    print("Model training complete.")

if os.path.exists(model_path):
    model = load_model(model_path)
else:
    print("Model not found. Triggering training process...")
    train_model()
    model = load_model(model_path)  # Load the newly trained model
    
# Helper function to get file extension
def get_file_extension(filename):
    return os.path.splitext(filename)[1]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Get the file extension from the original file
    file_extension = get_file_extension(file.filename)
    
    # Refactor the file name to the current epoch time with original extension
    epoch_time = int(time.time())
    filename = f"{epoch_time}{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({"image_path": file_path}), 200


@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        # Get the image path from request
        data = request.get_json()
        img_path = data['image_path']
        
        # Load and preprocess the image
        image = Image.open(img_path)
        image = image.resize((30, 30))
        image = np.expand_dims(np.array(image), axis=0)
        
        # Predict
        pred = np.argmax(model.predict(image), axis=1)[0]
        sign = classes[pred + 1]
        
        # Return the prediction
        return jsonify({"sign": sign})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5007)
