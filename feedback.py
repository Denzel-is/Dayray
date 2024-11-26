from flask import Blueprint, render_template, request, redirect,session
from models import db, Feedback

feedback_bp = Blueprint('feedback', __name__)

def get_reviews_from_db():
    # Получаем все записи из таблицы Feedback
    reviews = Feedback.query.all()
    
    # Преобразуем данные в нужный формат
    formatted_reviews = [{'cust_name': review.cust_name, 
                          'feedback_text': review.feedback_text, 
                          'feedback_date': review.feedback_date} 
                         for review in reviews]
    
    return formatted_reviews

@feedback_bp.route('/feedback')
def feedback():
    reviews = get_reviews_from_db()
    return render_template('feedback.html', feedbacks=reviews)

@feedback_bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    # Получаем имя пользователя из сессии
    name = session.get('username')
    # Получаем текст отзыва из формы
    feedback_text = request.form['feedback']
    
    # Создаем новый отзыв
    new_feedback = Feedback(cust_name=name, feedback_text=feedback_text)
    
    # Добавляем отзыв в сессию и сохраняем в базе данных
    db.session.add(new_feedback)
    db.session.commit()
    
    # Перенаправляем пользователя на страницу с отзывами
    return redirect('/feedback')
