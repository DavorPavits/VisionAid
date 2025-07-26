import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO


#Initilize Flask app
app = Flask(__name__)


#Set route
@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"

#Upload image route
@app.route("/upload", methods=["GEt","POST"])
def upload_image():
    if request.method == "POSt":
        #Get Image from request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        f = request.files["file"]
        if f.filename == '':
            return jsonify({"error": "No selected file"}), 400
        f.save("uploaded_image.png")
        return jsonify({"message": "Image uploaded successfully"}), 200
    return jsonify({"message": "Send a POST request with an image file"}), 200
