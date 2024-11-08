from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os
import json
import openai
import numpy as np
from dotenv import load_dotenv  # Для загрузки переменных окружения

app = Flask(__name__)
CORS(app)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Установка API ключа OpenAI из переменной окружения
openai.api_key = os.getenv('OPENAI_API_KEY')

# Проверка, что API-ключ установлен
if openai.api_key:
    app.logger.info('API key successfully loaded.')
else:
    app.logger.error('API key not found. Please set OPENAI_API_KEY in your .env file.')

# Настройка логирования
if not os.path.exists('logs'):
    os.mkdir('logs')

# Используем ConcurrentRotatingFileHandler
file_handler = ConcurrentRotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('LAPKA Chat Bot startup')

# Загрузка данных из JSONL файла
DATA = []
with open('products_data.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        messages = item['messages']
        if len(messages) >= 2:
            user_message = messages[0]['content']
            assistant_message = messages[1]['content']
            DATA.append({
                'question': user_message.lower().strip(),
                'answer': assistant_message.strip()
            })

# Определение функции для получения эмбеддинга
def get_embedding(text, model="text-embedding-ada-002"):
    result = openai.Embedding.create(
        input=[text],
        model=model
    )
    embedding = result['data'][0]['embedding']
    return embedding

# Определение функции для вычисления косинусного сходства
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Создание эмбеддингов для базы знаний
embeddings = []
for item in DATA:
    question = item['question']
    embedding = get_embedding(question)
    embeddings.append({'embedding': embedding, 'item': item})

def find_relevant_items(user_question, top_k=3):
    user_embedding = get_embedding(user_question)
    similarities = []
    for entry in embeddings:
        entry_embedding = entry['embedding']
        similarity = cosine_similarity(user_embedding, entry_embedding)
        similarities.append((similarity, entry['item']))
    # Сортировка по убыванию схожести
    similarities.sort(key=lambda x: x[0], reverse=True)
    relevant_items = [item for _, item in similarities[:top_k]]
    return relevant_items

def generate_answer(user_question):
    relevant_items = find_relevant_items(user_question)
    knowledge = ""
    for item in relevant_items:
        knowledge += f"Q: {item['question']}\nA: {item['answer']}\n\n"
    
    # Создаем список сообщений для чат-комплита
    messages = [
        {"role": "system", "content": "Вы выступаете в роли ассистента зоомагазина 'LAPKA'. Используйте только приведенную ниже информацию о товарах для ответа на вопрос пользователя. Не добавляйте информацию из других источников."},
        {"role": "system", "content": f"Информация о товарах:\n{knowledge}"},
        {"role": "user", "content": user_question}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Убедитесь, что у вас есть доступ к этой модели
        messages=messages,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None,
    )
    answer = response['choices'][0]['message']['content'].strip()
    return answer

@app.route('/')
def index():
    app.logger.info('html page accessed')
    return render_template('check_api.html')  # Убедитесь, что файл chat.html находится в папке templates

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        app.logger.warning('No JSON data provided in chat request')
        return jsonify({"error": "No JSON data provided."}), 400

    user_message = data.get("message", "").strip()
    if not user_message:
        app.logger.warning('Empty message received in chat request')
        return jsonify({"error": "Message is empty."}), 400

    app.logger.info(f'Received chat request: {user_message}')

    # Генерируем ответ с помощью модели GPT
    try:
        answer = generate_answer(user_message)
        app.logger.info(f'Generated answer: {answer}')
        return jsonify({"reply": answer})
    except Exception as e:
        app.logger.error(f'Error generating answer: {e}')
        return jsonify({"reply": "Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже."})

if __name__ == "__main__":
    app.run(debug=True)
