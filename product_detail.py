from flask import Blueprint, render_template, request, jsonify, current_app, session
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
        return render_template('product_details.html', product=product, error_message=error_message)

    # Запрос на получение отзывов о продукте
    try:
        feedback_response = requests.get(f"{FEEDBACK_API_URL}?productId={id}")
        feedback_response.raise_for_status()
        feedbacks = feedback_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе отзывов: {e}")
        feedbacks = []
        error_message = "Не удалось загрузить отзывы о продукте."

    # Обработка отправки отзыва
    if request.method == 'POST':
        # Проверка на добавление отзыва
        if 'rating' in request.form and 'comment' in request.form:
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

            # После добавления отзыва обновим список отзывов
            try:
                feedback_response = requests.get(f"{FEEDBACK_API_URL}?productId={id}")
                feedback_response.raise_for_status()
                feedbacks = feedback_response.json()
                print(f"feed")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при повторном запросе отзывов: {e}")
                feedbacks = []

            return render_template(
                'product_details.html',
                product=product,
                feedbacks=feedbacks,
                feedback_message=feedback_message
            )

        # Обработка отправки формы для добавления в корзину
        elif 'quantity' in request.form:
            quantity = int(request.form['quantity'])

            # Проверяем, что количество не превышает доступное
            if quantity > product['count']:
                error_message = f"Вы не можете выбрать больше {product['count']} товаров."
                return render_template(
                    'product_details.html',
                    product=product,
                    feedbacks=feedbacks,
                    error_message=error_message
                )

            # Здесь можно продолжить процесс добавления товара в корзину (например, через API или сессию)

    return render_template('product_details.html', product=product, feedbacks=feedbacks)
