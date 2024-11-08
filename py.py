from flask import Flask, render_template
from config import Config
from auth import auth_bp
from products import products_bp
from cart import cart_bp
from feedback import feedback_bp
from database import connectionbd
from pay import pay_bp
app = Flask(__name__)
app.config.from_object(Config)

# Регистрация blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(pay_bp)


@app.route('/')
def mainp():
    connection = connectionbd()
    cursor = connection.cursor()
    cursor.execute('SELECT name, map, links FROM categories')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('html.html', postgres_data=data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
