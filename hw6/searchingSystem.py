import math
import os
import pymorphy3
from nltk import word_tokenize
from os import listdir, path

LEMMAS_PATH = path.dirname('/Users/olga/PycharmProjects/info-search/hw2/processed_results/')
TF_IDF_PATH = path.dirname('/Users/olga/PycharmProjects/info-search/hw4/result/lemmas/')
INDEX_PATH = '/Users/olga/PycharmProjects/info-search/hw3/inverted_index.txt'

class SearchingSystem:

    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer()
        self.index = self.get_index()
        self.lemmas = self.get_lemmas()
        self.documents_lemmas_tf_idf = dict()
        self.lemmas_documents_tf_idf = dict()
        self.document_lengths = dict()
        self.get_lemmas_tf_idf()
        self.calc_document_vector_length()

    def get_index(self):
        index = dict()
        with open(INDEX_PATH, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            for line in lines:
                index[line.split(" ", 1)[0]] = set(eval(line.split(" ", 1)[1]))
        return index

    def get_lemmas(self):
        lemmas_dict = dict()
        for file_name in listdir(LEMMAS_PATH):
            with open(LEMMAS_PATH + '/' + file_name, 'r', encoding='utf-8', errors='ignore') as lemmas:
                lines = lemmas.read().splitlines()
                for l in lines:
                    parts = l.split(" ")
                    key = parts[0]
                    values = parts[1:]

                    if key in lemmas_dict:
                        lemmas_dict[key].extend(v for v in values if v not in lemmas_dict[key])
                    else:
                        lemmas_dict[key] = values
        return lemmas_dict

    def get_lemmas_tf_idf(self):
        for file_name in listdir(TF_IDF_PATH):
            with open(TF_IDF_PATH + '/' + file_name, encoding='utf-8') as tf_idf_file:
                lines = tf_idf_file.readlines()
                for line in lines:
                    data = line.rstrip('\n').split(' ')

                    lemma_to_documents_tf_idf = self.lemmas_documents_tf_idf.get(data[0], {})
                    lemma_to_documents_tf_idf[file_name] = float(data[2])
                    self.lemmas_documents_tf_idf[data[0]] = lemma_to_documents_tf_idf

                    documents_to_lemma_tf_idf = self.documents_lemmas_tf_idf.get(file_name, {})
                    documents_to_lemma_tf_idf[data[0]] = float(data[2])
                    self.documents_lemmas_tf_idf[file_name] = documents_to_lemma_tf_idf

    def calc_document_vector_length(self):
        for doc in os.listdir(TF_IDF_PATH):
            self.document_lengths[doc] = math.sqrt(sum(i ** 2 for i in self.documents_lemmas_tf_idf[doc].values()))

    def multiply_vectors(self, query_vector, document_vector, document_vector_length):
        return sum(document_vector.get(token, 0) for token in query_vector) / len(query_vector) / document_vector_length

    def search(self, query):
        query_vector = [self.morph.parse(token)[0].normal_form for token in word_tokenize(query, language='russian')]
        documents = set()
        for lemma in query_vector:
            documents = documents.union(self.index.get(lemma, set()))
        result = dict()
        for doc in documents:
            tf_idf_doc = doc.split('-')[1].split(".")[0] + '_lemmas.txt'
            result[doc] = self.multiply_vectors(query_vector, self.documents_lemmas_tf_idf[tf_idf_doc], self.document_lengths[tf_idf_doc])
        return sorted(result.items(), key=lambda r: r[1], reverse=True)


if __name__ == '__main__':
    search_system = SearchingSystem()
    while True:
        user_input = input("Введите запрос: ")
        if user_input == 'exit':
            exit()
        print(search_system.search(user_input))
