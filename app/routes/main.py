from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁路由
    輸入：無
    邏輯：顯示系統介紹
    輸出：渲染 index.html
    """
    pass

@main_bp.route('/dashboard')
def dashboard():
    """
    儀表板路由
    輸入：Session 中的 user_id
    邏輯：驗證登入，撈取個人的所有歷史紀錄
    輸出：渲染 dashboard.html
    """
    pass
