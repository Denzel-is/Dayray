from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Order, PaymentMethod
from datetime import datetime
from cart import get_cart_data
from cart import remove_from_cart_db  
from models import Cart, Product, db  # Предполагается, что Product - это модель для таблицы products

pay_bp = Blueprint('pay', __name__)

@pay_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    print("Получен запрос", request.method)
    user_id = session.get('customer_id')
    print("user_id : ", user_id)

    # Получаем данные из корзины
    cart_data = get_cart_data(user_id)
    print("cart_data : ", cart_data)
    total = sum(item['price'] * item['quantity'] for item in cart_data)
    print("total : ", total)

    if request.method == 'POST':
        # Проверка данных
        if not user_id:
            print("Ошибка: пользователь не найден!")
            return "Ошибка: пользователь не найден!", 400
        
        if total <= 0:
            print("Ошибка: некорректная сумма заказа!")
            return "Ошибка: некорректная сумма заказа!", 400

        # Создание нового заказа
        new_order = Order(
            customer_id=user_id,
            total_amount=total,
            status='Pending',
            order_date=datetime.now()
        )
        try:
            db.session.add(new_order)
            db.session.commit()
            print(f"Заказ успешно добавлен, order_id: {new_order.order_id}")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при добавлении заказа: {e}")
            return f"Ошибка при создании заказа: {e}", 500

        # Сохраняем order_id и total в сессии
        session['order_id'] = new_order.order_id
        session['total'] = total

        # Перенаправляем на страницу для обработки платежа
        return redirect(url_for('pay.process_payment'))
    
    # При GET запросе `order_id` отсутствует
    return render_template('pay.html', cart_data=cart_data, total=total, order_id=None)

@pay_bp.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    user_id = session.get('customer_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    # Получаем данные из сессии
    order_id = session.get('order_id')
    total = session.get('total')

    if not order_id or not total:
        print(f"Ошибка: отсутствуют обязательные параметры. order_id={order_id}, total={total}")
        return "Ошибка: order_id или total не переданы!", 400

    if request.method == 'POST':
        address = request.form.get('address')
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_expiry = request.form.get('card_expiry')
        card_cvv = request.form.get('card_cvv')

        print(f"Получены данные для обработки платежа: order_id={order_id}, total={total}")
        
        try:
            # Проверяем, существует ли активный заказ
            active_order = Order.query.filter_by(order_id=order_id, customer_id=user_id, status='Pending').first()
            if not active_order:
                print(f"Ошибка: активный заказ с order_id={order_id} не найден!")
                return "Активный заказ не найден", 400

            # Обработка срока действия карты
            expiry_parts = card_expiry.split('/')
            if len(expiry_parts) != 2 or not all(part.isdigit() for part in expiry_parts):
                return "Ошибка: некорректный формат срока действия карты!", 400
            
            expiry_date = datetime(int('20' + expiry_parts[1]), int(expiry_parts[0]), 1)

            # Сохранение метода оплаты
            new_payment_method = PaymentMethod(
                customer_id=user_id,
                card_holder_name=card_name,
                card_number=card_number,
                card_expiry_date=expiry_date,
                card_cvv=card_cvv,
                address=address
            )
            db.session.add(new_payment_method)

            # Обновляем статус заказа
            active_order.status = 'Paid'
            db.session.commit()
            
            print(f"Платеж успешно обработан. order_id={order_id}")
            # Очистить данные в сессии
            session.pop('order_id', None)
            session.pop('total', None)

            return redirect(url_for('pay.success'))
        
        except Exception as e:
            print(f"Ошибка при обработке платежа: {e}")
            db.session.rollback()
            return f"Ошибка при обработке платежа: {e}", 500

    return render_template('pay.html')

@pay_bp.route('/success')
def success():
    # Получаем customer_id из сессии (или откуда-то еще, если это необходимо)
    customer_id = session.get('customer_id')  # Предполагаем, что customer_id хранится в сессии

    if customer_id:
        # Получаем список товаров из корзины, хранящейся в сессии
        Cart.query.filter_by(customer_id=customer_id).delete()
        db.session.commit()
        db.session.rollback()
    # Устанавливаем статус платежа в сессии
    session['payment_status'] = 'Платеж успешно обработан!'

    # Перенаправление на главную страницу
    return redirect(url_for('mainp'))
