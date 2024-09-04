from flask import Flask, request, jsonify, render_template
import requests
import spacy
import nltk
from nltk.corpus import wordnet

app = Flask(__name__)

API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

# Load the spaCy model for NLP tasks
nlp = spacy.load("en_core_web_sm")

# Preprocess the text to enhance query understanding
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

# Get the meaning of a word from the dictionary API
def get_word_meaning(word):
    response = requests.get(f"{API_URL}{word}")
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Content: {response.text}")
    if response.status_code == 200:
        data = response.json()
        return data[0]['meanings'][0]['definitions'][0]['definition']
    else:
        return "Sorry, the word is not found in the dictionary."

# Get synonyms and antonyms using WordNet
def get_synonyms_antonyms(word):
    try:
        synonyms = []
        antonyms = []

        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name())

        print(f"Synonyms: {synonyms}")
        print(f"Antonyms: {antonyms}")
        return set(synonyms), set(antonyms)
    except Exception as e:
        print(f"Error fetching synonyms/antonyms: {e}")
        return set(), set()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_meaning', methods=['POST'])
def get_meaning():
    try:
        user_input = request.json.get('text', '')
        print(f"User input: {user_input}")
        processed_input = preprocess_text(user_input)
        print(f"Processed input: {processed_input}")
        word = processed_input.split()[-1]
        print(f"Word to look up: {word}")

        meaning = get_word_meaning(word)
        print(f"Meaning: {meaning}")

        synonyms, antonyms = get_synonyms_antonyms(word)
        print(f"Synonyms: {synonyms}")
        print(f"Antonyms: {antonyms}")

        response = {
            'meaning': meaning,
            'synonyms': ', '.join(synonyms),
            'antonyms': ', '.join(antonyms)
        }

        return jsonify({'response': response})

    except Exception as e:
        print(f"Error: {e}")  # Print error to console
        return jsonify({'error': 'An error occurred. Please check the server logs for details.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
