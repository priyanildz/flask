from flask import Flask, render_template, request
from parrot import Parrot
from spellchecker import SpellChecker
from textblob import TextBlob
import torch
import warnings

app = Flask(__name__)
warnings.filterwarnings("ignore")

# Initialize Parrot model
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

# Initialize Spell Checker
spell_checker = SpellChecker()

# Uncomment below to get reproducible paraphrase generations
'''
def random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

random_state(1234)
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paraphrase', methods=['GET', 'POST'])
def paraphrase():
    if request.method == 'POST':
        phrase = request.form['phrase']
        corrected_phrase = ' '.join([spell_checker.correction(word) for word in phrase.split()])
        para_phrases = parrot.augment(input_phrase=corrected_phrase)
        return render_template('paraphrase.html', phrase=phrase, para_phrases=para_phrases)
    return render_template('paraphrase.html')

@app.route('/spelling', methods=['GET', 'POST'])
def spelling():
    if request.method == 'POST':
        phrase = request.form['phrase']
        corrected_phrase = ' '.join([spell_checker.correction(word) for word in phrase.split()])
        return render_template('spelling.html', phrase=phrase, corrected_phrase=corrected_phrase)
    return render_template('spelling.html')

@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        phrase = request.form['phrase']
        analysis = TextBlob(phrase)
        sentiment = analysis.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        if polarity > 0:
            sentiment_label = "Positive"
        elif polarity < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        return render_template('sentiment.html', phrase=phrase, sentiment_label=sentiment_label, polarity=polarity, subjectivity=subjectivity)

    return render_template('sentiment.html')

if __name__ == '__main__':
    app.run(debug=True)
