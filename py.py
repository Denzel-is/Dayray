from flask import Flask, render_template, session, redirect, url_for
from config import Config
from auth import auth_bp
from products import products_bp
from cart import cart_bp
from feedback import feedback_bp
from pay import pay_bp
from models import db, Category, Product, Reg
from flask_migrate import Migrate
#from ai import ai_bp
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

# Регистрация blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(pay_bp, url_prefix='/payments')
#app.register_blueprint(ai_bp)

# Главная страница
@app.route('/')
def mainp():
    # Получаем сообщение из сессии, если оно есть
    payment_status = session.pop('payment_status', None)  # Убираем сообщение из сессии после отображения

    # Получаем данные категорий из базы данных
    data = Category.query.all()

    # Отправляем данные в шаблон
    return render_template('html.html', postgres_data=data, payment_status=payment_status)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
