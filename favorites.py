# favorites.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import requests

favorites_bp = Blueprint('favorites', __name__)
FAVORITES_API_URL = "http://localhost:5107/api/favorites"

@favorites_bp.route('/favorites', methods=['GET'])
def view_favorites():
    """
    Страница «Избранное»: показывает товары, которые пользователь добавил в избранное.
    """
    token = session.get('token')
    if not token:
        # Перенаправляем на логин, если не авторизован
        return redirect(url_for('login.login'))
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        # Пример ожидаемого ответа:
        # {
        #   "favoriteItems": [
        #       {"productId": 1, "productName": "Товар1", "productPrice": 500, "productImageUrl": "..."},
        #       ...
        #   ]
        # }
        resp = requests.get(FAVORITES_API_URL, headers=headers)
        resp.raise_for_status()
        favorites_data = resp.json()

        favorite_items = favorites_data.get('favoriteItems', [])
        return render_template('favorites.html', favorite_items=favorite_items)
    except requests.RequestException as e:
        print(f"Ошибка получения «Избранного»: {e}")
        # Если произошла ошибка, вернём пустой список
        return render_template('favorites.html', favorite_items=[])

@favorites_bp.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    token = session.get('token')
    if not token:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({"success": False, "error": "No product_id provided"}), 400

    headers = {'Authorization': f'Bearer {token}'}
    params = {'productId': product_id}

    try:
        # Убираем /add
        resp = requests.post(FAVORITES_API_URL, headers=headers, params=params)
        resp.raise_for_status()
        return jsonify({"success": True})
    except requests.RequestException as e:
        print(f"Ошибка добавления в «Избранное»: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@favorites_bp.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    token = session.get('token')
    if not token:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({"success": False, "error": "No product_id provided"}), 400

    headers = {'Authorization': f'Bearer {token}'}
    params = {'productId': product_id}

    try:
        # Удаление через DELETE:
        resp = requests.delete(FAVORITES_API_URL, headers=headers, params=params)
        resp.raise_for_status()
        return jsonify({"success": True})
    except requests.RequestException as e:
        print(f"Ошибка удаления из «Избранное»: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@favorites_bp.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    """
    Удаление товара из «Избранного» (AJAX).
    Возвращаем JSON: {"success": True/False}.
    """
    token = session.get('token')
    if not token:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({"success": False, "error": "No product_id provided"}), 400

    headers = {'Authorization': f'Bearer {token}'}
    params = {'productId': product_id}

    try:
        resp = requests.post(f"{FAVORITES_API_URL}/remove", headers=headers, params=params)
        resp.raise_for_status()
        return jsonify({"success": True})
    except requests.RequestException as e:
        print(f"Ошибка удаления из «Избранного»: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
