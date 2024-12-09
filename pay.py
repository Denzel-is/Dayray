from flask import Blueprint, render_template, request, redirect, url_for, jsonify,session
import requests

pay_bp = Blueprint('pay', __name__)

API_PAYMENT_URL = "http://localhost:5107/api/payment"
API_CART_URL = "http://localhost:5107/api/cart/clear"  # URL для очистки корзины

@pay_bp.route('/payment', methods=['GET', 'POST'])
def process_payment():
    if request.method == 'GET':
        # Параметры: ID заказа и сумма
        order_id = request.args.get('order_id', default=0, type=int)
        total = request.args.get('total', default=0.0, type=float)

        # Проверка, если order_id или total равны нулю
        if order_id == 0 or total == 0.0:
            return "Ошибка: неверные данные о заказе", 400

        # Передаем данные в шаблон для рендеринга
        return render_template('pay.html', order_id=order_id, total=total)

    elif request.method == 'POST':
        # Получаем данные из формы
        order_id = request.form.get('order_id')
        total = request.form.get('total')
        address = request.form.get('address')
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_expiry = request.form.get('card_expiry')
        card_cvv = request.form.get('card_cvv')
        print(f"PayData: {total}")

        # Проверка, что все обязательные поля заполнены
        if not order_id or not total or not address or not card_name or not card_number or not card_expiry or not card_cvv:
            return "Ошибка: все поля должны быть заполнены", 400

        # Формируем JSON-данные для API
        try:
            payment_data = {
                "orderId": int(order_id),
                "amount": float(total),
                "address": address,
                "cardName": card_name,
                "cardNumber": card_number,
                "cardExpiry": card_expiry,
                "cardCVV": card_cvv
            }
        except ValueError:
            return "Ошибка: неверный формат данных", 400

        try:
            # Отправляем POST-запрос к API платежей
            response = requests.post(f"{API_PAYMENT_URL}/process-payment", json=payment_data)

            # Проверяем статус ответа
            response.raise_for_status()
            payment_response = response.json()

            # Обрабатываем успешный платеж
            payment_id = payment_response.get("payment_id") if isinstance(payment_response, dict) else payment_response
            token = session.get('token')  # Токен для авторизации
        
            headers = {'Authorization': f'Bearer {token}'}
            
            if payment_id:
                userId = session.get('token')
              
                cart_clear_response = requests.post(f"{API_CART_URL}", headers=headers)
                cart_clear_response.raise_for_status()
                session.pop('cart', None)
                return redirect(url_for('pay.success', payment_id=payment_id))
            else:
                return "Ошибка: не удалось получить ID платежа", 500

        except requests.RequestException as e:
            print(f"Ошибка при обработке платежа: {e}")
            return "Ошибка при обработке платежа", 500

@pay_bp.route('/success')
def success():
    payment_id = request.args.get('payment_id')
    if not payment_id:
        return "Ошибка: ID платежа не найден", 400
    return render_template('success.html', payment_id=payment_id)

