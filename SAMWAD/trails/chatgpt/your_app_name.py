from flask import Flask, render_template, request
from parrot import Parrot
import torch
import warnings

warnings.filterwarnings("ignore")

# Initialize Flask app
app = Flask(__name__)

# Initialize Parrot model
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

# Function to generate paraphrases
def generate_paraphrases(phrase):
    para_phrases = parrot.augment(input_phrase=phrase)
    return para_phrases

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        phrase = request.form['phrase']
        paraphrases = generate_paraphrases(phrase)
        return render_template('index.html', paraphrases=paraphrases, input_phrase=phrase)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
