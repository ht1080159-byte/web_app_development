from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊路由
    GET 邏輯：渲染 register.html 表單
    POST 邏輯：接收表單資料，驗證並建立 User，完成後重導向 login
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入路由
    GET 邏輯：渲染 login.html 表單
    POST 邏輯：接收表單資料，驗證密碼，寫入 session，成功重導向 dashboard
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    登出路由
    邏輯：清除 session 中的 user_id，重導向首頁
    """
    pass
