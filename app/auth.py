from flask import Blueprint, render_template, request, redirect, url_for, session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'user' and password == 'pass':
            session['user'] = username
            return redirect(url_for('main.dashboard'))
        elif username == 'admin' and password == 'admin':
            session['user'] = username
            return redirect(url_for('admin.admin_panel'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))