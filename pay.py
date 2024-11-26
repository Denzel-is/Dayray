from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, PaymentMethod, Transaction, Order
from datetime import datetime
from cart import get_cart_data

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

        # Передаем идентификатор нового заказа для обработки платежа
        return redirect(url_for('pay.process_payment', order_id=new_order.order_id, total=total))
    
    return render_template('pay.html', cart_data=cart_data, total=total, order_id=new_order.order_id)



@pay_bp.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    user_id = session.get('customer_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Логируем данные, полученные из формы
        order_id = request.form.get('order_id')
        print(f"Получен order_id: {order_id}")  # Логируем получение order_id

        if not order_id:
            return "Ошибка: order_id не передан!", 400
        
        total = float(request.form.get('total', 0))
        address = request.form.get('address')
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_expiry = request.form.get('card_expiry')
        card_cvv = request.form.get('card_cvv')

        print(f"Получены данные для обработки платежа (POST): order_id={order_id}, total={total}")
        print(f"Дополнительные данные: address={address}, card_name={card_name}, card_number={card_number}, card_expiry={card_expiry}, card_cvv={card_cvv}")

        try:
            # Проверяем, существует ли активный заказ
            active_order = Order.query.filter_by(order_id=order_id, customer_id=user_id, status='Pending').first()
            if not active_order:
                print(f"Ошибка: активный заказ с order_id={order_id} для пользователя {user_id} не найден!")
                return "Активный заказ не найден", 400

            # Обработка платежа
            return redirect(url_for('pay.success'))
        except Exception as e:
            print(f"Ошибка при обработке платежа: {e}")
            db.session.rollback()
            return f"Ошибка при обработке платежа: {e}", 500



@pay_bp.route('/success')
def success():
    return "Платеж успешно обработан!"
