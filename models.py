from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    stock_quantity = db.Column(db.Integer)
    map_p = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=True)  # Внешний ключ
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    product_suppliers = db.relationship('ProductSupplier', backref='product', lazy=True)

    category = db.relationship('Category', backref='products')

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    map = db.Column(db.String(100))
    


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)


class Customer(db.Model):
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    

    


class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('reg.customer_id'))
    order_date = db.Column(db.DateTime, server_default=db.func.now())
    total_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='Pending')
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    transaction = db.relationship('Transaction', backref='order', uselist=False)


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Numeric(8, 2))


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    product_suppliers = db.relationship('ProductSupplier', backref='supplier', lazy=True)


class ProductSupplier(db.Model):
    __tablename__ = 'product_suppliers'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), primary_key=True)
    unit_price = db.Column(db.Numeric(8, 2))


class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    
    payment_method_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('reg.customer_id'))
    card_holder_name = db.Column(db.String(100))
    card_number = db.Column(db.String(16))
    card_expiry_date = db.Column(db.Date)
    card_cvv = db.Column(db.String(4))
    address = db.Column(db.Text)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    transaction_date = db.Column(db.DateTime, server_default=db.func.now())
    payment_method = db.Column(db.String(50))
    amount_paid = db.Column(db.Numeric(10, 2))
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.payment_method_id'))


class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('reg.customer_id'))
    feedback_text = db.Column(db.Text)
    cust_name = db.Column(db.String(100))
    feedback_date = db.Column(db.Date, server_default=db.func.now())


class Employee(db.Model):
    __tablename__ = 'employees'
    
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Numeric(10, 2))
    hire_date = db.Column(db.Date)


class EmployeeSchedule(db.Model):
    __tablename__ = 'employee_schedule'
    
    schedule_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


class Cart(db.Model):
    __tablename__ = 'cart'
    
    cart_id = db.Column(db.Integer, primary_key=True)
    link_c = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('reg.customer_id'))
    quantity = db.Column(db.Integer, default=1)

class Log(db.Model):
    __tablename__ = 'log'
    
    login_id = db.Column(db.Integer, primary_key=True)  # Идентификатор записи
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)  # Ссылка на пользователя
    login_time = db.Column(db.DateTime, default=datetime.utcnow)  # Время входа (с текущим временем по умолчанию)
    success = db.Column(db.Boolean, nullable=False)  # Успешность входа
    
    customer = db.relationship('Customer', backref=db.backref('logins', lazy=True))  # Связь с таблицей customers
    
    def __repr__(self):
        return f'<Log {self.login_id} - Customer {self.customer_id}>'

class Reg(db.Model):
    __tablename__ = 'reg'
    
    customer_id = db.Column(db.Integer, primary_key=True)  # Идентификатор пользователя
    first_name = db.Column(db.String(100), nullable=False)  # Имя
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email (уникальный)
    phone_number = db.Column(db.String(20))  # Номер телефона
    city = db.Column(db.String(50))  # Город
    username = db.Column(db.String(50), unique=True, nullable=False)  # Имя пользователя (уникальное)
    hashed_password = db.Column(db.String(255), nullable=False)  # Хэшированный пароль
    address = db.Column(db.Text)  # Адрес
    role = db.Column(db.String(20), nullable=False)  # Добавлено значение по умолчанию "user"

    # Добавьте любые другие связи или методы, которые могут понадобиться

    def __repr__(self):
        return f'<Reg {self.customer_id} - {self.username}>'