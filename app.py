from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader
from gtts import gTTS
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    pdf_file = request.files['pdf']

    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)

    reader = PdfReader(pdf_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    audio_path = os.path.join(AUDIO_FOLDER, "output.mp3")

    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)