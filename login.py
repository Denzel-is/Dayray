from flask import Blueprint, render_template, request, current_app, jsonify, session,redirect
import requests
from config import Config

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    API_URL = current_app.config['API_URL']
    LOGIN_API_URL = API_URL + "/Account/login"
    
    """
    Страница входа, обрабатывает форму и возвращает токен, если аутентификация успешна.
    """
    if request.method == 'POST':
        # Получаем данные из формы
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        try:
            # Запрос к API для проверки данных
            response = requests.post(LOGIN_API_URL, json={'username': username, 'password': password})
            response.raise_for_status()  # Проверка на успешность запроса
        
            # Проверка на наличие токена в ответе
            if response.ok:
                # Сохраняем имя пользователя в session
                session['username'] = username
                session['token'] = response.json().get('token')
                session['user_id'] = response.json().get('userId')  # Сохраняем userId

                # Возвращаем ответ с токеном и именем пользователя
                return jsonify({'token': session['token'], 'username': session['username']})

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе API: {e}")
            return jsonify({'error': 'Неверный логин или пароль'}), 401

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)    
    session.pop('customer_id', None)
    session.pop('cart', None)
    return redirect('/')