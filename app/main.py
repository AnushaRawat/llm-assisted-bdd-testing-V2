from flask import Blueprint, render_template, request, session, redirect, url_for

main = Blueprint('main', __name__)

requests_db = []

@main.route('/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', requests=requests_db)
    
@main.route('/submit', methods=['POST'])
def submit_request():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    req_text = request.form.get('request_text')
    if req_text:
        requests_db.append({'id': len(requests_db) + 1, 'text': req_text, 'status': 'Pending'})
    return redirect(url_for('main.dashboard'))