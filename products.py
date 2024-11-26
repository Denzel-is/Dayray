from flask import Blueprint, render_template, request
from models import Product,  Category

products_bp = Blueprint('products', __name__)

def fetch_products(category_id=None, query=None):
    # Если есть поисковый запрос
    products_query = Product.query
    if category_id:
        products_query = products_query.filter(Product.category_id == category_id)
    if query:
        products_query = products_query.filter(Product.name.ilike(f"%{query}%"))

    products = products_query.all()

    # Преобразуем в список словарей для передачи в шаблон
    return [{
        'product_id': product.product_id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock_quantity': product.stock_quantity,
        'map_p': product.map_p
    } for product in products]

def fetch_product_details(product_id):
    product = Product.query.filter_by(product_id=product_id).first()

    # Преобразуем объект продукта в словарь
    if product:
        return {
            'product_id': product.product_id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock_quantity': product.stock_quantity,
            'map_p': product.map_p
        }
    return None


@products_bp.route('/products')
def products():
    query = request.args.get('query')
    category_id = request.args.get('category_id', type=int)

    data = fetch_products(category_id, query)
    categories = Category.query.all()  # Получаем все категории для фильтрации

    return render_template('products.html', postgres_data=data, categories=categories)
    
@products_bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = fetch_product_details(product_id)
    if product:
        return render_template('prods.html',
                               product_id=product['product_id'],
                               product_name=product['name'],
                               product_description=product['description'],
                               product_price=product['price'],
                               product_stock=product['stock_quantity'],
                               product_image_url=product['map_p'])
    else:
        return "Продукт не найден", 404
