import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
from nltk.util import ngrams
from collections import Counter

nltk.download('stopwords')
stopwords_en = set(stopwords.words('english'))

def tokenize(document):
    document = document.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = [token for token in tokenizer.tokenize(document) if token not in stopwords_en]
    return tokens

def tokenize_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    chapter = soup.find("div", class_="chapter", id="ch01")
    
    if chapter:
        chapter_text = chapter.get_text(separator="\n", strip=True).lower()
        return tokenize(chapter_text)
    else:
        print("Chapter not found in the HTML file.")
        return []

def load_pickle_file(pickle_file_path):
    try:
        with open(pickle_file_path, "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        print(f"Pickle file {pickle_file_path} not found.")
        return []

def generate_candidates(tokens, n_max=3):
    candidates = []
    for n in range(1, n_max + 1):
        ngram_candidates = list(ngrams(tokens, n))
        candidates.extend([' '.join(ngram) for ngram in ngram_candidates])
    return candidates

def casing_feature(keyword):
    return any(word[0].isupper() for word in keyword.split())

def word_position_feature(keyword, tokens):
    words = keyword.split()
    first_word_pos = tokens.index(words[0]) if words[0] in tokens else -1
    return 1 / (first_word_pos + 1) if first_word_pos != -1 else 0

def word_frequency_feature(keyword, tokens):
    count = tokens.count(keyword)
    return count / len(tokens)

def word_relatedness_feature(keyword, tokens, window_size=5):
    words = keyword.split()
    related_count = 0
    for i, word in enumerate(tokens):
        if word == words[0]:
            window = tokens[i+1:i+1+window_size]
            related_count += sum(1 for w in words[1:] if w in window)
    return related_count

def context_dispersion_feature(keyword, tokens, window_size=5):
    words = keyword.split()
    positions = [i for i, word in enumerate(tokens) if word == words[0]]
    dispersion_score = 0
    for pos in positions:
        window = tokens[pos:pos+window_size]
        dispersion_score += sum(1 for w in words[1:] if w in window)
    return dispersion_score / len(positions) if positions else 0

def score_candidates(candidates, tokens):
    scored_candidates = []
    for candidate in candidates:
        f1 = casing_feature(candidate)
        f2 = word_position_feature(candidate, tokens)
        f3 = word_frequency_feature(candidate, tokens)
        f4 = word_relatedness_feature(candidate, tokens)
        f5 = context_dispersion_feature(candidate, tokens)
        
        score = f1 + f2 + f3 + f4 + f5
        scored_candidates.append((candidate, score))
    return scored_candidates

def rank_keywords_by_frequency(candidates, tokens):
    frequency = Counter(tokens)
    ranked_keywords = [(keyword, frequency[keyword]) for keyword in candidates if keyword in frequency]
    ranked_keywords = sorted(ranked_keywords, key=lambda x: x[1], reverse=True)
    return ranked_keywords

# Inference code
html_file_path = "/Users/Raneet/Desktop/imitatingYake/resource/pg75577-images.html"
pickle_file_path = "/Users/Raneet/Desktop/imitatingYake/stopWords/chapter_tokens.p"

html_tokens = tokenize_html_file(html_file_path)
print("Sample HTML Tokens:", html_tokens[:50])

chapter_tokens = load_pickle_file(pickle_file_path)
print("Sample Resume Tokens:", chapter_tokens[:50])

candidates = generate_candidates(html_tokens)
scored_candidates = score_candidates(candidates, html_tokens)
ranked_keywords = rank_keywords_by_frequency(candidates, html_tokens)

print("Top 15 Scored Candidates:", scored_candidates[:15])
print("Top 15 Ranked Keywords:", ranked_keywords[:15])