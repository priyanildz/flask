from flask import Flask, render_template, request
from parrot import Parrot
from spellchecker import SpellChecker
import torch
import warnings

app = Flask(__name__)
warnings.filterwarnings("ignore")

# Initialize Parrot model
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
spell_checker = SpellChecker()

# Function to generate paraphrases
def generate_paraphrases(phrase):
    para_phrases = parrot.augment(input_phrase=phrase)
    return para_phrases

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phrase = request.form['phrase']
        if 'paraphrase' in request.form:
            paraphrases = generate_paraphrases(phrase)
            return render_template('paraphrase.html', paraphrases=paraphrases, input_phrase=phrase)
        elif 'spelling' in request.form:
            corrected_phrase = ' '.join([spell_checker.correction(word) for word in phrase.split()])
            return render_template('spelling.html', phrase=phrase, corrected_phrase=corrected_phrase)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
