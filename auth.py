from flask import Blueprint, request, session, redirect, render_template,flash, url_for
from models import db, Reg 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Проверка сессии
    if 'username' in session:
        return redirect("/")  # Перенаправление на главную страницу

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Получаем пользователя из базы данных
        user = Reg.query.filter_by(username=username).first()

        if user and user.hashed_password == password:  # Проверьте пароль (здесь логика простая, обычно используется хеширование)
            # Установка сессии
            session['username'] = username
            session['customer_id'] = user.customer_id
            session['role'] = user.role

            flash('Успешный вход!', 'success')
            
            # Перенаправляем в админку, если роль администратора, иначе на главную
        
            return redirect(url_for('mainp'))  # Перенаправление на главную страницу

        flash('Неверный логин или пароль', 'danger')  # Сообщение об ошибке
    return render_template('login.html')
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']
        city = request.form['city']
        username = request.form['username']
        address = request.form['address']

        if password != confirm_password:
            return "Пароли не совпадают", 400

        # Проверяем, существует ли уже пользователь с таким email или username
        existing_user = Reg.query.filter((Reg.username == username) | (Reg.email == email)).first()
        if existing_user:
            return "Пользователь с таким именем или email уже существует", 400

        # Создаем нового пользователя
        new_user = Reg(
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            city=city,
            username=username,
            hashed_password=password,  # Здесь должна быть логика хеширования пароля
            address=address,
            role='user'
        )

        # Добавляем нового пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')  # Перенаправляем на страницу входа

    return render_template('registration.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('customer_id', None)
    session.pop('cart', None)
    return redirect('/')
