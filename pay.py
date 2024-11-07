from flask import Blueprint, render_template, request, redirect
from database import connectionbd

pay_bp = Blueprint('pay', __name__)

@pay_bp.route('/pay')
def pay():
    return render_template('pay.html')

pay_bp.route('/process_payment')
def process_payment():
    # Получение данных из формы...
    address = request.form.get('address')
    card_name = request.form.get('card_name')
    card_number = request.form.get('card_number')
    card_expiry = request.form.get('card_expiry')
    card_cvv = request.form.get('card_cvv')
   
    amount_paid = 100  # Пример
    order_id = 1       # Пример

    connection = connectionbd()
    cursor = connection.cursor()
    try:
        # Вставка данных карты в таблицу card_details
        cursor.execute("INSERT INTO card_details (card_number, card_expiry_date, card_cvv, card_holder_name) VALUES (%s, %s, %s, %s) RETURNING card_id", 
                       (card_number, card_expiry, card_cvv, card_name))
        card_id = cursor.fetchone()[0]

        # Вставка записи транзакции в таблицу transactions
        cursor.execute("INSERT INTO transactions (order_id, payment_method, amount_paid, card_id) VALUES (%s, %s, %s, %s)", 
                       (order_id, 'Credit Card', amount_paid, card_id))

        connection.commit()
    except Exception as e:
        print(f"Ошибка при обработке платежа: {e}")
        connection.rollback()  # Откат в случае ошибкиа
        # Дополнительная обработка ошибок
    finally:
        cursor.close()
        connection.close()

    return redirect("/")