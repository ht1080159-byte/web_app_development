from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊路由
    GET 邏輯：渲染 register.html 表單
    POST 邏輯：接收表單資料，驗證並建立 User，完成後重導向 login
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 基礎驗證
        if not username or not email or not password:
            flash('所有欄位都是必填的！', 'danger')
            return render_template('auth/register.html')
            
        # 檢查 Email 是否已存在
        existing_user = User.get_by_email(email)
        if existing_user:
            flash('該 Email 已經被註冊過！', 'danger')
            return render_template('auth/register.html')
            
        # 將密碼雜湊並建立使用者
        password_hash = generate_password_hash(password)
        user_id = User.create(username, email, password_hash)
        
        if user_id:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊時發生錯誤，請稍後再試。', 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入路由
    GET 邏輯：渲染 login.html 表單
    POST 邏輯：接收表單資料，驗證密碼，寫入 session，成功重導向 dashboard
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email 與密碼為必填！', 'danger')
            return render_template('auth/login.html')
            
        # 根據 Email 撈取使用者
        user = User.get_by_email(email)
        
        # 驗證密碼
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'歡迎回來，{user["username"]}！', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email 或密碼錯誤！', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    登出路由
    邏輯：清除 session 中的 user_id，重導向首頁
    """
    session.pop('user_id', None)
    session.pop('username', None)
    flash('您已成功登出。', 'success')
    return redirect(url_for('main.index'))
