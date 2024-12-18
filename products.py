from flask import Blueprint, render_template, request, current_app
import requests
from config import Config

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def products():
    API_URL = current_app.config['API_URL']
    PRODUCTS_API_URL = API_URL + "/Products"

    query = request.args.get('query', '')  # Получаем параметр поиска из URL
    category_id = request.args.get('categoryId', None) 
    params = {"query": query}
    if category_id:
        params["categoryId"] = category_id
    print(f"params{params}")
    # Добавляем параметр поиска в запрос к API
    try:
        response = requests.get(PRODUCTS_API_URL, params=params)
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        products = []
        error_message = "Не удалось загрузить продукты. Попробуйте позже."
        return render_template('products.html', products=products, error=error_message)
    
    return render_template('products.html', products=products)
