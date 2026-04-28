from flask import Flask
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    # 初始化 Flask 應用程式
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 應用程式設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-do-not-use-in-prod')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制最大上傳檔案為 16MB
    
    # 載入並註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.practice import practice_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(practice_bp)
    
    # 初始化資料庫 (確保資料庫檔案與資料表存在)
    with app.app_context():
        from app.models.db import init_db
        init_db()
        
    return app

if __name__ == '__main__':
    app = create_app()
    # 確保暫存錄音檔資料夾存在
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True, port=5000)
