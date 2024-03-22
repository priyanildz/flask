from flask import Flask, render_template, request, redirect, url_for
from google.cloud import speech_v1p1beta1 as speech
import os
from textblob import TextBlob
import language_tool_python

app = Flask(__name__)

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    # Convert audio to text using Google Cloud Speech-to-Text
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=file.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    # Analyze the text for grammatical errors using LanguageTool
    errors = tool.check(transcript)

    # Analyze the text for sentiment using TextBlob
    blob = TextBlob(transcript)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        sentiment = 'Positive'
    elif sentiment_score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return render_template('result.html', transcript=transcript, errors=errors, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
