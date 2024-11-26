from flask import Blueprint, request, session, redirect, render_template,url_for
from models import Cart, Product, db  # Предполагается, что Product - это модель для таблицы products

cart_bp = Blueprint('cart', __name__)


def get_cart_data(user_id):
    cart_items = Cart.query.filter_by(customer_id=user_id).all()
    cart_data = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            cart_data.append({
                'product_id': item.product_id,
                'name': product.name,
                'price': product.price,
                'quantity': item.quantity,
                'map_p': product.map_p
            })
    return cart_data

def clear_cart(user_id):
    try:
        # Удаляем товары из корзины для текущего пользователя
        Cart.query.filter_by(customer_id=user_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при очистке корзины: {e}")
def add_to_cart_db(product_id, customer_id):
    try:
        cart_item = Cart.query.filter_by(product_id=product_id, customer_id=customer_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(product_id=product_id, customer_id=customer_id, quantity=1)
            db.session.add(cart_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка в add_to_cart_db: {e}")

def remove_from_cart_db(product_id, customer_id):
    try:
        # Удаление записи из таблицы корзины для конкретного пользователя и товара
        Cart.query.filter_by(product_id=product_id, customer_id=customer_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при удалении товара из корзины: {e}")

def get_cart_data_from_db(cart_items):
    cart_data = []
    for product_id in cart_items:
        product = Product.query.get(product_id)
        if product:
            cart_data.append({
                'product_id': product_id,
                'name': product.name,
                'price': product.price,
                'image_url': product.map_p.replace('./static/', '/static/')
            })
    return cart_data

@cart_bp.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    customer_id = session.get('customer_id')
    current_quantity = get_product_quantity_from_cart(product_id)
    action = request.form.get('change')

    if action == 'increase':
        new_quantity = current_quantity + 1
    elif action == 'decrease' and current_quantity > 1:
        new_quantity = current_quantity - 1
    else:
        new_quantity = current_quantity

    update_cart_quantity(product_id, new_quantity, customer_id)
    return redirect(url_for('cart.cart'))

def get_product_quantity_from_cart(product_id):
    cart_item = Cart.query.filter_by(product_id=product_id).first()
    return cart_item.quantity if cart_item else 0 

def update_cart_quantity(product_id, new_quantity, customer_id):
    try:
        cart_item = Cart.query.filter_by(product_id=product_id, customer_id=customer_id).first()
        if cart_item:
            cart_item.quantity = new_quantity
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при обновлении количества товара в корзине: {e}")

@cart_bp.route('/cart')
def cart():
    customer_id = session.get('customer_id')
    cart_data = get_cart_data(customer_id)
    total = sum(float(item['price']) * item['quantity'] for item in cart_data)
    return render_template('cart.html', cart_data=cart_data, total=total)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        print("Ошибка: product_id не найден")
        return redirect(request.referrer or '/')

    product_id = int(product_id)
    print("СЕССИЯ",session.get('customer_id'))
    customer_id = session.get('customer_id')  # Идентификатор пользователя

    try:
        add_to_cart_db(product_id, customer_id)
    except Exception as e:
        print(f"Ошибка при добавлении товара в корзину: {e}")
        return redirect(request.referrer or '/')

    session.modified = True
    return redirect(request.referrer or '/')
@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('auth.login'))  # Перенаправление на страницу входа, если пользователь не авторизован

    # Удалить товар из корзины текущего пользователя в базе данных
    remove_from_cart_db(product_id, customer_id)
    
    # Обновить сессию, если корзина хранится и в сессии
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
        session.modified = True

    return redirect(url_for('cart.cart'))
