from flask import Blueprint, request, session, redirect, render_template,url_for
from database import connectionbd

cart_bp = Blueprint('cart', __name__)

def add_to_cart_db(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cart_id = 1  # Пример, замените на актуальный идентификатор корзины пользователя
        cursor.execute("INSERT INTO cart (cart_id, product_id) VALUES (%s, %s)", (cart_id, product_id))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при добавлении товара в корзину: {e}")
    finally:
        cursor.close()
        connection.close()

# Функция для удаления товара из корзины пользователя в базе данных
def remove_from_cart_db(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при удалении товара из корзины: {e}")
    finally:
        cursor.close()
        connection.close()

# Функция для получения данных о товарах в корзине пользователя из базы данных
def get_cart_data_from_db(cart_items):
    connection = connectionbd()
    cursor = connection.cursor()
    cart_data = []
    for product_id in cart_items:
        cursor.execute("SELECT name, price, map_p FROM products WHERE product_id = %s", (product_id,))
        product_data = cursor.fetchone()
        if product_data:
            cart_data.append({
                'product_id': product_id,
                'name': product_data[0],
                'price': product_data[1],
                'image_url': product_data[2].replace('./static/', '/static/')
            })
    cursor.close()
    connection.close()
    return cart_data

@cart_bp.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    current_quantity = get_product_quantity_from_cart(product_id)
    action = request.form.get('change')

    if action == 'increase':
        new_quantity = current_quantity + 1
    elif action == 'decrease' and current_quantity > 1:
        new_quantity = current_quantity - 1
    else:
        new_quantity = current_quantity

    update_cart_quantity(product_id, new_quantity)
    return redirect(url_for('cart'))
# Функция для получения количества определенного товара в корзине пользователя
def get_product_quantity_from_cart(product_id):
    connection = connectionbd()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT quantity FROM cart WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Ошибка при получении количества товара из корзины: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

# Функция для обновления количества товара в корзине пользователя
def update_cart_quantity(product_id, new_quantity):
    connection = connectionbd()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE cart SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при обновлении количества товара в корзине: {e}")
    finally:
        cursor.close()
        connection.close()
    pass


@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = []

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        if product_id:
            product_id = int(product_id)
        action = request.form.get('action')

        if action == 'add' and product_id not in session['cart']:
            session['cart'].append(product_id)
            add_to_cart_db(product_id)
        elif action == 'remove' and product_id in session['cart']:
            session['cart'].remove(product_id)
            remove_from_cart_db(product_id)

        session.modified = True

    cart_data = get_cart_data_from_db(session['cart'])
    total = sum(float(item['price']) for item in cart_data)
    return render_template('cart.html', cart_data=cart_data, total=total)
#     cart_data = get_cart_data_from_db(session['cart'])
#     total = sum(float(item['price']) * get_product_quantity_from_cart(item['product_id']) for item in cart_data)
#     return render_template('cart.html', cart_data=cart_data, total=total)
@cart_bp.route('/add_to_cart', methods=['POST'])

def add_to_cart():
    product_id = request.form.get('product_id')
    if product_id:
        product_id = int(product_id)
        if 'cart' not in session:
            session['cart'] = []
        if product_id not in session['cart']:
            session['cart'].append(product_id)
            add_to_cart_db(product_id)  
        session.modified = True
    return redirect(request.referrer or '/')

def add_to_cart_db(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cart_id = 1  # Пример, замените на актуальный идентификатор корзины пользователя
        cursor.execute("INSERT INTO cart (cart_id, product_id) VALUES (%s, %s)", (cart_id, product_id))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при добавлении товара в корзину: {e}")
    finally:
        cursor.close()
        connection.close()


@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if product_id in session.get('cart', []):
        session['cart'].remove(product_id)
        remove_from_cart_db(product_id)  # вызов функции удаления из БД
        session.modified = True

    return redirect(url_for('cart.cart'))
