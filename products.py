from flask import Blueprint, render_template, request, current_app, session
import requests

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def products():
 
    API_URL = current_app.config['API_URL']  # например, "http://localhost:5107/api"
    PRODUCTS_API_URL = API_URL + "/Products"  # => "http://localhost:5107/api/Products"

    # 1) Получаем токен из сессии
    token = session.get('token')
    
    # 2) Пытаемся вытащить товары из корзины (cart_item_ids)
    cart_item_ids = []
    if token:
        try:
            headers = {'Authorization': f'Bearer {token}'}
            cart_resp = requests.get(f"{API_URL}/cart", headers=headers)  # "http://localhost:5107/api/cart"
            cart_resp.raise_for_status()
            cart_data = cart_resp.json()
          
            cart_item_ids = [
                item.get('productId')
                for item in cart_data.get('cartItems', [])
            ]
            # Убедимся, что это числа (если в product.id тоже числа)
            cart_item_ids = [int(pid) for pid in cart_item_ids if pid is not None]
        except requests.RequestException as e:
            print(f"Ошибка при запросе корзины: {e}")
            cart_item_ids = []
    else:
        cart_item_ids = []

    # 3) Получаем список продуктов
    query = request.args.get('query', '')      # Параметр поиска
    category_id = request.args.get('categoryId', None) 
    params = {"query": query}
    if category_id:
        params["categoryId"] = category_id

    print(f"Параметры для /Products: {params}")
    
    products = []
    error_message = None
    try:
        response = requests.get(PRODUCTS_API_URL, params=params)
        response.raise_for_status()
        products = response.json()  # Список продуктов
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        error_message = "Не удалось загрузить продукты. Попробуйте позже."

    for p in products:
        if isinstance(p["id"], str):
            p["id"] = int(p["id"])

    return render_template(
        'products.html',
        products=products,
        cart_item_ids=cart_item_ids,
        error=error_message
    )
