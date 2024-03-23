from parrot import Parrot
from spellchecker import SpellChecker
import torch
import warnings

warnings.filterwarnings("ignore")

'''
uncomment to get reproducible paraphrase generations
def random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

random_state(1234)
'''

# Initialize models (make sure you initialize ONLY once if you integrate this into your code)
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
spell_checker = SpellChecker()

phrases = ["Can you recommend some upscale restaurants in New York?",
           "What are the famous places we should not miss in Russia?"
           ]

for phrase in phrases:
    print("-" * 100)
    print("Input_phrase: ", phrase)
    print("-" * 100)
    
    # Check and correct spelling errors
    corrected_phrase = ' '.join([spell_checker.correction(word) for word in phrase.split()])
    print("Corrected Input Phrase:", corrected_phrase)
    
    para_phrases = parrot.augment(input_phrase=corrected_phrase)
    for para_phrase in para_phrases:
        print(para_phrase)
