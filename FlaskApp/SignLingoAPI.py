from flask import Flask, request, send_file, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api', methods=['POST'])
def api():
    video = request.files
    video = video['video'].read()
    #video = request.form['video']
    # video2 = request.files['video']
    print(video)
    
    return render_template("display.html", video=video)
    #return send_file(video)