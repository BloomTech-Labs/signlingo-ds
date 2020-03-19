from flask import Flask

def create_app():
    
    app = Flask(__name__)

    @app.route('/')
    def root():
        return ("<h1>Welcome to Sign-Lingo!</h1>")

    return app