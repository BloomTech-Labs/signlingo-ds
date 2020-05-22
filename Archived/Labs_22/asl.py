import tensorflow as tf
import numpy as np
from flask import Flask, request, jsonify
from models import best_current_model
from utilities import process_img


model = best_current_model()  # created upon deployment instead of every call of predict

/*
def create_app():
    
    app = Flask(__name__)

    @app.route('/')
    def root():
        return "<h1>Welcome to Sign-Lingo!</h1>"

    @app.route('/model', methods=['POST'])
    def predict():
        """
        This endpoint takes an uploaded image and returns prediction confidences for each class which can then be routed
        to the activity api for determining feedback and next steps.
        """
        image_file = request.files['file']
        processed_image = process_img(image_file)
        output = model.predict([[processed_image]])
        output = output.tolist()  # plays nice with JSONIFY
        return jsonify(output)

    return app
*/
