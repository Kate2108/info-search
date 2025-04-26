from flask import Flask, render_template, request, jsonify
from searchingSystem import SearchingSystem

app = Flask(__name__)

# Инициализация поисковой системы
search_system = SearchingSystem()

def get_relevance_label(score):
    """Определяем метку релевантности по score"""
    if score > 0.8:
        return "Очень высокая"
    elif score > 0.5:
        return "Высокая"
    elif score > 0.2:
        return "Средняя"
    return "Низкая"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})

    results = search_system.search(query)
    formatted_results = [{
        'document': doc,
        'score': f"{score:.4f}",
        'relevance': get_relevance_label(score)  # Используем функцию без self
    } for doc, score in results if score > 0]  # Фильтруем нулевые результаты

    return jsonify({'results': formatted_results})

if __name__ == '__main__':
    app.run(debug=True)