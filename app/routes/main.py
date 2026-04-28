from flask import Blueprint, render_template, session, redirect, url_for
from app.models.record import Record

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁路由"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """儀表板路由"""
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    # 取得歷史紀錄
    records = Record.get_by_user(user_id)
    return render_template('dashboard.html', records=records)
