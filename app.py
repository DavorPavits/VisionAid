import pathlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from fastai.vision.all import load_learner, PILImage
import traceback
from flasgger import Swagger


#Initilize Flask app
app = Flask(__name__)
swagger = Swagger(app)

CORS(app, origins=["http://localhost:5173"])

#Load the pre-trained model
learn_inf = load_learner("model/object_model.pkl")

#Upload image route
@app.route("/", methods=["POST", "OPTIONS"])
def upload_and_predict():
    """Endpoint to upload an image and get predictions.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file to be uploaded for prediction.
    responses:
      200:
        description: A successful response with the prediction results.
        schema:
          type: object
          properties:
            prediction:
              type: string
              example: cat
            probability:
              type: number
              format: float
              example: 0.95
    """
    if request.method == "OPTIONS":
        return '', 200 
    
    if request.method == "POST":
        #Get Image from request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        

        f = request.files["file"]
        if f.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        #Predict without saving
        try:
            print("Received file:", f.filename)
            f.save("temp_image.jpg")  # Save the image temporarily if needed
            img = PILImage.create(f)
            print("Predicting...")
            

            
            pred, pred_ix, probs = learn_inf.predict(img)
            print(f"Prediction: {pred}, Index: {pred_ix}, Probabilities: {probs}")
            return jsonify({
                'prediction': str(pred),
                'probability': float(probs[pred_ix])
            })
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
