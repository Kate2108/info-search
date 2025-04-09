import os
import math
from collections import Counter, defaultdict


def load_lemma_mappings(filepath):
    lemma_map = defaultdict(list)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                elements = line.strip().split()
                if elements:
                    lemma_map[elements[0]] = elements[1:]
    except:
        return defaultdict(list)
    return lemma_map


def compute_term_frequencies(terms):
    if not terms:
        return {}
    term_counts = Counter(terms)
    total_terms = len(terms)
    return {term: count / total_terms for term, count in term_counts.items()}


def compute_inverse_document_frequencies(documents):
    document_count = len(documents)
    if document_count == 0:
        return {}

    term_document_freq = defaultdict(int)
    for document in documents:
        for term in set(document):
            term_document_freq[term] += 1

    return {term: math.log((document_count + 1) / (freq + 1)) + 1
            for term, freq in term_document_freq.items()}


def process_documents():
    input_dir = "../hw2/processed_results"
    output_dir = "result"

    os.makedirs(f"{output_dir}/terms", exist_ok=True)
    os.makedirs(f"{output_dir}/lemmas", exist_ok=True)

    doc_ids = {f.split('-')[-1].split('.')[0]
               for f in os.listdir(input_dir)
               if f.startswith("lemmas_download-")}

    document_data = []
    for doc_id in doc_ids:
        lemma_file = f"{input_dir}/lemmas_download-{doc_id}.txt"
        token_file = f"{input_dir}/tokens_download-{doc_id}.txt"

        try:
            lemma_map = load_lemma_mappings(lemma_file)
            with open(token_file, 'r', encoding='utf-8') as f:
                tokens = [line.strip() for line in f if line.strip()]
            document_data.append((doc_id, lemma_map, tokens))
        except:
            continue

    term_idf = compute_inverse_document_frequencies([doc[2] for doc in document_data])
    lemma_idf = compute_inverse_document_frequencies([list(doc[1].keys()) for doc in document_data])

    for doc_id, lemmas, tokens in document_data:
        try:
            with open(f"{output_dir}/terms/{doc_id}_terms.txt", 'w', encoding='utf-8') as f:
                for term, tf in compute_term_frequencies(tokens).items():
                    idf = term_idf.get(term, 0.0)
                    f.write(f"{term} {idf:.4f} {tf * idf:.4f}\n")

            if tokens:
                with open(f"{output_dir}/lemmas/{doc_id}_lemmas.txt", 'w', encoding='utf-8') as f:
                    for lemma, words in lemmas.items():
                        tf = sum(1 for token in tokens if token in words) / len(tokens)
                        idf = lemma_idf.get(lemma, 0.0)
                        f.write(f"{lemma} {idf:.4f} {tf * idf:.4f}\n")
        except:
            pass


if __name__ == "__main__":
    process_documents()