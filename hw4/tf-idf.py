import os
import re
from collections import defaultdict
from math import log

# Пути к данным
HTML_DIR = "../hw1/pages/"  # HTML-документы
PROCESSED_RESULTS_DIR = "../hw2/processed_results/"  # Леммы и токены
OUTPUT_DIR = "results"  # Директория для выходных файлов

# Регулярное выражение для очистки текста
TEXT_CLEANER = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

# Создание директории для выходных данных
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


# Чтение токенов и лемм для конкретного документа
def read_tokens_and_lemmas(doc_id):
    tokens_file = os.path.join(PROCESSED_RESULTS_DIR, f"tokens_download-{doc_id}.txt")
    lemmas_file = os.path.join(PROCESSED_RESULTS_DIR, f"lemmas_download-{doc_id}.txt")

    tokens = set()
    lemmas = defaultdict(set)

    # Чтение токенов
    if os.path.exists(tokens_file):
        with open(tokens_file, 'r', encoding='utf-8') as f:
            for line in f:
                token = line.strip()
                if token:
                    tokens.add(token)

    # Чтение лемм
    if os.path.exists(lemmas_file):
        with open(lemmas_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) > 1:
                    lemma = parts[0]
                    forms = parts[1:]
                    lemmas[lemma].update(forms)

    return tokens, lemmas


# Извлечение текста из HTML
def extract_text_from_html(html_content):
    cleaned_text = TEXT_CLEANER.sub('', html_content)
    return cleaned_text.lower()


# Подсчет TF
def calculate_tf(text, terms):
    term_counts = defaultdict(int)
    total_terms = 0

    for word in text.split():
        if word in terms:
            term_counts[word] += 1
            total_terms += 1

    tf = {term: count / total_terms for term, count in term_counts.items()}
    return tf


# Подсчет IDF
def calculate_idf(documents, terms):
    doc_count = defaultdict(int)
    total_docs = len(documents)

    for doc in documents:
        unique_terms = set(doc.split())
        for term in unique_terms:
            if term in terms:
                doc_count[term] += 1

    idf = {term: log(total_docs / (count + 1)) for term, count in doc_count.items()}
    return idf


# Сохранение результатов в файл
def save_results(filename, data):
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
        for term, (idf, tf_idf) in data.items():
            f.write(f"{term} {idf} {tf_idf}\n")


# Основная функция
def main():
    # Чтение HTML-файлов
    html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
    documents = []

    for html_file in html_files:
        with open(os.path.join(HTML_DIR, html_file), 'r', encoding='utf-8') as f:
            html_content = f.read()
            text = extract_text_from_html(html_content)
            documents.append(text)

    # Обработка каждого документа
    for idx, html_file in enumerate(html_files):
        doc_id = idx + 1  # Номер документа (от 1 до 100)
        text = documents[idx]

        # Чтение токенов и лемм для текущего документа
        tokens, lemmas = read_tokens_and_lemmas(doc_id)

        # Подсчет IDF для токенов и лемм
        token_idf = calculate_idf(documents, tokens)
        lemma_idf = calculate_idf(documents, {form for forms in lemmas.values() for form in forms})

        # Подсчет TF для токенов
        token_tf = calculate_tf(text, tokens)
        token_tf_idf = {token: (token_idf.get(token, 0), token_tf[token] * token_idf.get(token, 0))
                        for token in token_tf}

        # Подсчет TF для лемм
        lemma_tf = calculate_tf(text, {form for forms in lemmas.values() for form in forms})
        lemma_tf_idf = {}
        for lemma, forms in lemmas.items():
            lemma_count = sum(lemma_tf.get(form, 0) for form in forms)
            if lemma_count > 0:
                lemma_idf_value = max(lemma_idf.get(form, 0) for form in forms)
                lemma_tf_idf[lemma] = (lemma_idf_value, lemma_count * lemma_idf_value)

        # Сохранение результатов
        base_name = os.path.splitext(html_file)[0]
        save_results(f"{base_name}_tokens.txt", token_tf_idf)
        save_results(f"{base_name}_lemmas.txt", lemma_tf_idf)


if __name__ == "__main__":
    main()