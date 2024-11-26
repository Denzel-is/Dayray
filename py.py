from flask import Flask, render_template, session, redirect, url_for
from config import Config
from auth import auth_bp
from products import products_bp
from cart import cart_bp
from feedback import feedback_bp
from pay import pay_bp
from models import db, Category, Product, Reg
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from wtforms.validators import DataRequired
from prodAdmin import ProductAdminView
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
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

class AdminModelView(ModelView):
    def is_accessible(self):
        # Проверка, есть ли пользователь в сессии и если его роль 'admin'
        if 'role' not in session or session['role'] != 'admin':
            return False  # Доступ закрыт
        return True  # Доступ разрешен только для админов

    def inaccessible_callback(self, name, **kwargs):
        # Если нет доступа, перенаправляем на страницу логина или главную
        return redirect(url_for('mainp'))

admin.add_view(ProductAdminView(Product, db.session))
admin.add_view(ModelView(Category, db.session))  

@app.route('/')
def mainp():
    data = Category.query.all()
    return render_template('html.html', postgres_data=data)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
