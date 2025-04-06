from os import listdir, path
from bs4 import BeautifulSoup

PAGES_PATH = path.dirname('D:/Study/info-search/hw1/pages/')
LEMMAS_PATH = path.dirname('D:/Study/info-search/hw2/processed_results/')
INVERTED_INDEX_PATH = 'D:/Study/info-search/hw3/inverted_index.txt'

def get_texts():
    texts = dict()
    for file_name in listdir(PAGES_PATH):
        html = open(PAGES_PATH + '/' + file_name, 'r', encoding='utf-8', errors='ignore')
        text = BeautifulSoup(html, features='html.parser').get_text().lower()
        html.close()
        texts[file_name] = text
    return texts


def get_lemmas():
    lemmas_dict = dict()
    for file_name in listdir(LEMMAS_PATH):
        lemmas = open(LEMMAS_PATH + '/' + file_name, 'r', encoding='utf-8', errors='ignore')
        lines = lemmas.read().splitlines()
        lemmas.close()
        for l in lines:
            parts = l.split()
            lemmas_dict[parts[0]] = parts[1:]
    return lemmas_dict


def set_inverted_index():
    inverted_index = {}
    lemmas_data = get_lemmas()
    texts_data = get_texts()

    for lemma_key, lemma_list in lemmas_data.items():
        for file_name, text in texts_data.items():
            if any(lemma in text for lemma in lemma_list):
                inverted_index.setdefault(lemma_key, set()).add(file_name)

    for lemma in inverted_index:
        inverted_index[lemma] = list(inverted_index[lemma])

    with open(INVERTED_INDEX_PATH, 'w', encoding='utf-8') as index_file:
        for lemma, files in inverted_index.items():
            index_file.write(f"{lemma} {files}\n")

if __name__ == "__main__":
    set_inverted_index()