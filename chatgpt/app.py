from flask import Flask, render_template, request
import speech_recognition as sr
from language_tool_python import LanguageTool
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            tool = LanguageTool('en-US')
            matches = tool.check(text)
            errors = len(matches)
            sentiment = TextBlob(text).sentiment.polarity

            return render_template('result.html', text=text, errors=errors, sentiment=sentiment)

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)
