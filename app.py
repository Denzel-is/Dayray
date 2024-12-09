from flask import Flask, render_template, request
from products import products_bp
from login import login_bp
from product_detail import product_detail_bp
from cart import cart_bp
from pay import pay_bp
from ai import ai_bp
import requests
from config import Config
from registration import registration_bp  # Импорт Blueprint

app = Flask(__name__)
app.config.from_object(Config)

CATEGORIES_API_URL = app.config['API_URL'] + "/Categories"

app.register_blueprint(products_bp)
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(product_detail_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(ai_bp)


@app.route('/')
def index():
    """
    Главная страница. Получает категории с API и передает их в шаблон.
    """
    try:
        # Запрос к API для получения категорий
        response = requests.get(CATEGORIES_API_URL)
        response.raise_for_status()
        categories = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        categories = []
        error_message = "Не удалось загрузить категории. Попробуйте позже."
        return render_template('index.html', categories=categories, error=error_message)
    
    return render_template('index.html', categories=categories)





if __name__ == "__main__":
    app.run(debug=True)
