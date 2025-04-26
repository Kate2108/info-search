from flask import Flask, render_template, request, jsonify
from searchingSystem import SearchingSystem
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация поисковой системы
try:
    search_system = SearchingSystem()
    logger.info("Search system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize search system: {str(e)}")
    raise

def get_relevance_label(score):
    """Определяем метку релевантности по score"""
    try:
        score = float(score)
        if score > 0.8:
            return "Очень высокая"
        elif score > 0.5:
            return "Высокая"
        elif score > 0.2:
            return "Средняя"
        return "Низкая"
    except ValueError:
        return "Не определена"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '').strip()
        logger.info(f"Received search query: '{query}'")

        if not query:
            return jsonify({'results': []})

        results = search_system.search(query)
        formatted_results = []

        for doc, score in results[:10]:  # Берем топ-10
            try:
                if score > 0:
                    formatted_results.append({
                        'document': doc,
                        'score': f"{float(score):.4f}",
                        'relevance': get_relevance_label(score)
                    })
            except Exception as e:
                logger.error(f"Error processing result {doc}: {str(e)}")
                continue

        logger.info(f"Found {len(formatted_results)} results for query '{query}'")
        return jsonify(formatted_results)  # Убрали вложенность 'results' и 'total'

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)