import stanza
import nltk
import string
import json
from collections import Counter

nltk.download('punkt')
stanza.download('uk')
nlp = stanza.Pipeline('uk', processors='tokenize,mwt,pos,lemma')

with open("stopwords_ua_set.txt", encoding="utf-8") as f:
    stopwords_raw = f.read()
    ukrainian_stopwords = eval(stopwords_raw)

def preprocess(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation + '–—…“”«»0123456789'))
    return text

def analyze_text(text):
    text = preprocess(text)
    doc = nlp(text)
    lemmas = []

    for sentence in doc.sentences:
        for word in sentence.words:
            lemma = word.lemma
            if lemma.isalpha() and lemma not in ukrainian_stopwords:
                lemmas.append(lemma)

    return Counter(lemmas)

if __name__ == '__main__':
    text = input("Input >>>\n")
    full_freq_dict = analyze_text(text)

    print("\nTop 10:\n")
    for word, freq in full_freq_dict.most_common(10):
        print(f"{word}: {freq}")

    with open("frequency_dictionary.json", "w", encoding="utf-8") as json_file:
        json.dump(full_freq_dict, json_file, ensure_ascii=False, indent=4)
