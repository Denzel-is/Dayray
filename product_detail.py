from flask import Blueprint, render_template, request, jsonify, current_app,session
import requests

product_detail_bp = Blueprint('product_detail', __name__)

# Маршрут для страницы продукта
@product_detail_bp.route('/product/<int:id>', methods=['GET', 'POST'])
def product_details(id):
    API_URL = current_app.config['API_URL']
    PRODUCT_API_URL = f"{API_URL}/Products/{id}"
    FEEDBACK_API_URL = f"{API_URL}/Feedback"

    # Запрос на получение данных о продукте
    try:
        response = requests.get(PRODUCT_API_URL)
        response.raise_for_status()
        product = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        product = None
        error_message = "Не удалось загрузить данные о продукте. Попробуйте позже."
        return render_template('product_details.html', product=product, error=error_message)

    # Обработка отправки отзыва
    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        user_id = session.get("user_id")

        feedback_data = {
            'productId': id,
            'rating': rating,
            'comment': comment,
            'userId': user_id
        }

        try:
            response = requests.post(FEEDBACK_API_URL, json=feedback_data)
            response.raise_for_status()
            feedback_message = "Отзыв успешно отправлен!"
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке отзыва: {e}")
            feedback_message = "Произошла ошибка при отправке отзыва. Попробуйте снова позже."

        return render_template('product_details.html', product=product, feedback_message=feedback_message)

    return render_template('product_details.html', product=product)

