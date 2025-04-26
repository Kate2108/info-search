from flask import Flask, render_template, request, jsonify
from searchingSystem import SearchingSystem

app = Flask(__name__)

# Инициализация поисковой системы
search_system = SearchingSystem()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})

    results = search_system.search(query)
    # Форматируем результаты для вывода
    formatted_results = [{'document': doc, 'score': f"{score:.4f}"} for doc, score in results]
    return jsonify({'results': formatted_results})


if __name__ == '__main__':
    app.run(debug=True)