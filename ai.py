from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
CORS(app)

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Pet Store Chat Bot startup')

# Product catalog data
CATALOG = [
    {
        "question": "Что вы можете сказать о Корм Eukanuba для активных собак?",
        "answer": "Полноценный и сбалансированный корм для собак с повышенной активностью, обогащенный необходимыми витаминами и минералами. Цена: 5300.00$. В наличии: 25 шт."
    },
    {
        "question": "Что вы можете сказать о Корм Purina One для пожилых собак?",
        "answer": "Специализированный корм для пожилых собак, поддерживающий здоровье и активность на протяжении всей жизни. Цена: 4500.00$. В наличии: 40 шт."
    },
    # ... Add all other products here ...
    {
        "question": "Что вы можете сказать о Клетка EcoBird Natural Habitat?",
        "answer": "Экологически чистая клетка, имитирующая естественную среду обитания птиц. Цена: 10000.00$. В наличии: 6 шт."
    }
]

@app.route('/')
def index():
    app.logger.info('Index page accessed')
    return render_template('check_api.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        app.logger.warning('No JSON data provided in chat request')
        return jsonify({"error": "No JSON data provided."}), 400

    user_message = data.get("message", "").strip().lower()
    if not user_message:
        app.logger.warning('Empty message received in chat request')
        return jsonify({"error": "Message is empty."}), 400

    app.logger.info(f'Received chat request: {user_message}')

    # Search for the most relevant answer in the catalog
    best_match = None
    best_match_words = 0
    for item in CATALOG:
        question_words = set(item["question"].lower().split())
        message_words = set(user_message.split())
        common_words = question_words.intersection(message_words)
        if len(common_words) > best_match_words:
            best_match = item
            best_match_words = len(common_words)

    if best_match:
        app.logger.info(f'Found match for query: {user_message}')
        return jsonify({"reply": best_match["answer"]})
    else:
        app.logger.warning(f'No match found for query: {user_message}')
        return jsonify({"reply": "Извините, я не нашел информацию по вашему запросу. Попробуйте задать вопрос иначе."})

if __name__ == "__main__":
    app.run(debug=True)