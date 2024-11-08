from flask import Blueprint, render_template, request, redirect,session
from database import connectionbd

feedback_bp = Blueprint('feedback', __name__)

def get_reviews_from_db():
    connection = connectionbd()
    cursor = connection.cursor()
    cursor.execute("SELECT cust_name, feedback_text, feedback_date FROM feedback")
    reviews = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{'cust_name': row[0], 'feedback_text': row[1], 'feedback_date': row[2]} for row in reviews]

@feedback_bp.route('/feedback')
def feedback():
    reviews = get_reviews_from_db()
    return render_template('feedback.html', feedbacks=reviews)

@feedback_bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = session.get('username')
    feedback = request.form['feedback']
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO feedback (cust_name, feedback_text) VALUES (%s, %s)", (name, feedback))
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    return redirect('/feedback')
