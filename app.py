import os

from flask import Flask, render_template, request, send_file, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-question", methods=["GET"])
def get_question():
    question_filename = "question.wav"
    return send_from_directory(
        directory=os.path.dirname(question_filename),
        as_attachment=True,
        path=question_filename,
    )


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    audio = request.files["audio"]
    if audio:
        filename = "answer.wav"
        if os.path.exists(filename):
            os.remove(filename)
        audio.save(os.path.join("", filename))
        return "Audio saved", 200
    return "No audio found", 400


@app.route("/say-message", methods=["POST"])
def welcome_message():
    filename = "received_audio.wav"
    # return audio as attachment
    # send 200 status code
    if os.path.exists(filename):
        print("file exists")
    return send_file(filename, mimetype="audio/wav", as_attachment=True), 200


if __name__ == "__main__":
    app.run(debug=True)
