from flask import Blueprint, render_template, request
from database import connectionbd

products_bp = Blueprint('products', __name__)

def fetch_products(category_id, query=None):
    connection = connectionbd()
    cursor = connection.cursor()
    if query:
        cursor.execute("SELECT product_id, name, description, price, stock_quantity, map_p FROM products WHERE product_id IN (SELECT product_id FROM product_categories WHERE category_id = %s) AND name ILIKE %s", (category_id, '%' + query + '%'))
    else:
        cursor.execute("SELECT product_id, name, description, price, stock_quantity, map_p FROM products WHERE product_id IN (SELECT product_id FROM product_categories WHERE category_id = %s)", (category_id,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
def fetch_product_details(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    cursor.execute("SELECT product_id,name, description, price, stock_quantity, map_p FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()
    return product


@products_bp.route('/cats')
def cats():
    query = request.args.get('query')
    data = fetch_products(2, query)
    return render_template('catc.html', postgres_data=data)

@products_bp.route('/dogs')
def dogs():
    query = request.args.get('query')
    data = fetch_products(1, query)
    return render_template('catd.html', postgres_data=data)
@products_bp.route('/rodents')
def rodents():
    query = request.args.get('query')
    data = fetch_products(3, query)
    return render_template('catr.html', postgres_data=data)

@products_bp.route('/birds')
def birds():
    query = request.args.get('query')
    data = fetch_products(4, query)
    return render_template('catb.html', postgres_data=data)

@products_bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = fetch_product_details(product_id)
    if product:
        print(product[5],flush=True)
        return render_template('prods.html',
                               product_id=product[0],
                               product_name=product[1],
                               product_description=product[2],
                               product_price=product[3],
                               product_stock=product[4],
                               product_image_url=product[5])
    else:
        return "Продукт не найден", 404

