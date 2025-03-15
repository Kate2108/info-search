import os
import shutil
import urllib.request
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://lenta.ru/'
REQUEST_URL = 'https://lenta.ru/parts/news'
CLASS_ATTRIBUTE = 'card-full-news _parts-news'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_FOLDER = os.path.join(BASE_DIR, 'pages')
INDEX_FILE_NAME = os.path.join(BASE_DIR, 'index.txt')


def prepare_pages_folder():
    if os.path.exists(PAGES_FOLDER):
        shutil.rmtree(PAGES_FOLDER)

    os.makedirs(PAGES_FOLDER)

def prepare_index_file():
    with open(INDEX_FILE_NAME, 'w', encoding='utf-8') as f:
        f.write('')


def find_pages():
    links = []
    for i in range(1, 6):
        url = f"{REQUEST_URL}/{i}/"
        with urllib.request.urlopen(url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            a_tags = soup.find_all('a', {'class': CLASS_ATTRIBUTE})
            for a in a_tags:
                links.append(a.get('href'))
    return links


def get_text_from_page(url):
    response = requests.get(BASE_URL + url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all(['style', 'link', 'script']):
        tag.decompose()
    return str(soup)

def download_pages(count=100):
    links = list(set(find_pages()))
    with open(INDEX_FILE_NAME, 'w', encoding='utf-8') as index_file:
        page_number = 1
        for link in links:
            if page_number > count:
                break
            text = get_text_from_page(link)
            if not text:
                continue
            page_file_name = os.path.join(PAGES_FOLDER, f"download-{page_number}.html")
            with open(page_file_name, 'w', encoding='utf-8') as page_file:
                page_file.write(text)
            index_file.write(f"{page_number} {BASE_URL}{link}\n")
            page_number += 1

def main():
    prepare_pages_folder()
    prepare_index_file()
    download_pages()

if __name__ == '__main__':
    main()