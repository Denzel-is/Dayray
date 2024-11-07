from flask import Blueprint, request, session, redirect, render_template
from database import connectionbd

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Проверка сессии
    if 'username' in session:
        return redirect("/")  # Перенаправление на главную страницу

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = connectionbd()
        cursor = connection.cursor()

        hashed_password = password  # Здесь должна быть логика хеширования пароля

        try:
            cursor.execute("SELECT * FROM reg WHERE username = %s AND hashed_password = %s", (username, hashed_password))
            user = cursor.fetchall()
            if user:
                # Установка сессии
                session['username'] = username
                return redirect("/")  # Перенаправление на главную страницу

            return "Неверное имя пользователя или пароль", 401
        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return "Ошибка при входе", 500
        finally:
            cursor.close()
            connection.close()

    return render_template('/login.html')

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

        connection = connectionbd()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO reg (first_name, email, phone_number, city, username, hashed_password, address) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (first_name, email, phone_number, city, username, password, address))
            connection.commit()
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return "Ошибка при регистрации", 500
        finally:
            cursor.close()
            connection.close()

        return redirect('/login')

    return render_template('registration.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
