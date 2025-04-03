import os
import re
import nltk
from pymorphy3 import MorphAnalyzer
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")

morph_analyzer = MorphAnalyzer()

stop_words = set(stopwords.words("russian"))

input_directory = "../hm1/pages"
output_directory = "processed_results"
os.makedirs(output_directory, exist_ok=True)

russian_word_pattern = re.compile(r"^[а-яА-ЯёЁ]+$")

def process_html_files():
    for file_name in os.listdir(input_directory):
        full_path = os.path.join(input_directory, file_name)
        with open(full_path, "r", encoding="utf-8") as input_file:
            html_data = input_file.read()
            plain_text = extract_text_from_html(html_data)
            token_set = extract_russian_tokens(plain_text)

        token_output_path = os.path.join(output_directory, f"tokens_{file_name}")
        with open(token_output_path, "w", encoding="utf-8") as token_file:
            token_file.write("\n".join(sorted(token_set)))

        lemma_dict = group_by_lemma(token_set)
        lemma_output_path = os.path.join(output_directory, f"lemmas_{file_name}")
        with open(lemma_output_path, "w", encoding="utf-8") as lemma_file:
            for base, words in sorted(lemma_dict.items()):
                lemma_file.write(f"{base} {' '.join(sorted(words))}\n")

if __name__ == "__main__":
    process_html_files()

def group_by_lemma(word_set):
    lemma_groups = {}
    for word in word_set:
        base_form = morph_analyzer.parse(word)[0].normal_form
        if base_form in lemma_groups:
            lemma_groups[base_form].add(word)
        else:
            lemma_groups[base_form] = {word}
    return lemma_groups

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_text = soup.get_text(separator=" ", strip=True)
    cleaned_text = re.sub(r'\s+', ' ', raw_text)
    return cleaned_text

def extract_russian_tokens(text_data):
    tokens = word_tokenize(text_data, language="russian")
    filtered_tokens = {
        token.lower() for token in tokens
        if russian_word_pattern.match(token) and token.lower() not in stop_words
    }
    return filtered_tokens