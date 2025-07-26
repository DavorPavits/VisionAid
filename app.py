import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO


#Initilize Flask app
app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])



#Upload image route
@app.route("/", methods=["GET","POST", "OPTIONS"])
def upload_image():
    if request.method == "OPTIONS":
        return '', 200 
    
    if request.method == "POST":
        #Get Image from request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        f = request.files["file"]
        if f.filename == '':
            return jsonify({"error": "No selected file"}), 400
        f.save("uploaded_image.png")
        return jsonify({"message": "Image uploaded successfully"}), 200
    return jsonify({"message": "Send a POST request with an image file"}), 200
