from flask import Blueprint, render_template, redirect, url_for, session
from .main import requests_db

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_panel():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin.html', requests=requests_db)

@admin.route('/approve/<int:req_id>')
def approve_request(req_id):
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('auth.login'))
    for req in requests_db:
        if req['id'] == req_id:
            req['status'] = 'Approved'
    return redirect(url_for('admin.admin_panel'))
