from flask import Flask, request
from .models import initial_model
from .utilities import process_img

model = initial_model()  # created upon deployment instead of every call of predict


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
        return model.predict([[processed_image]])

    return app
