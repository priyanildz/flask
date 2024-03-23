from textblob import TextBlob
from flask import Flask, request, render_template

app = Flask(__name__)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text.
    Returns a string indicating sentiment polarity.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Negative"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        text = request.form['text']
        sentiment = analyze_sentiment(text)
        return render_template('index.html', text=text, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
