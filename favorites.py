from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import requests

favorites_bp = Blueprint('favorites', __name__)
FAVORITES_API_URL = "http://localhost:5107/api/Favorites"

@favorites_bp.route('/favorites', methods=['GET'])
def view_favorites():
    """
    Страница «Избранное»: показывает товары, которые пользователь добавил в избранное.
    """
    token = session.get('token')
    if not token:
        return redirect(url_for('login.login'))
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        resp = requests.get(FAVORITES_API_URL, headers=headers)
        resp.raise_for_status()
        favorites_data = resp.json()
        print(f"productName {favorites_data}")

        if isinstance(favorites_data, list):
            favorite_items = favorites_data  
        else:
            favorite_items = []  

        return render_template('favorites.html', favorite_items=favorite_items)
    except requests.RequestException as e:
        print(f"Ошибка получения «Избранного»: {e}")
        return render_template('favorites.html', favorite_items=[])

@favorites_bp.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    """
    Добавление товара в избранное через API.
    """
    token = session.get('token')
    if not token:
        return redirect(url_for('login.login'))

    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({"success": False, "error": "No product_id provided"}), 400
    print(f"product_id {product_id}")

    headers = {'Authorization': f'Bearer {token}'}
    json_data = {'ProductId': product_id}  


    try:
        resp = requests.post(FAVORITES_API_URL, headers=headers, json=json_data)
        resp.raise_for_status()
        return redirect(url_for('favorites.view_favorites'))
    except requests.RequestException as e:
        print(f"Ошибка добавления в «Избранное»: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    

@favorites_bp.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    """
    Удаление товара из избранного через API.
    """
    token = session.get('token')
    if not token:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({"success": False, "error": "No product_id provided"}), 400
    headers = {'Authorization': f'Bearer {token}'}
    json_data = {'productId': product_id}

    try:
        resp = requests.delete(f"{FAVORITES_API_URL}/{product_id}", headers=headers, json=json_data)
        resp.raise_for_status()
        return redirect(url_for('favorites.view_favorites'))
    except requests.RequestException as e:
        print(f"Ошибка удаления из «Избранного»: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
