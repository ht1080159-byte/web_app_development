from flask import Blueprint

practice_bp = Blueprint('practice', __name__)

@practice_bp.route('/practice/topics')
def topics():
    """
    題庫列表路由
    邏輯：撈取所有主題並渲染列表
    輸出：渲染 topics.html
    """
    pass

@practice_bp.route('/practice/<int:topic_id>')
def practice_topic(topic_id):
    """
    口說測驗頁面
    輸入：URL 參數 topic_id
    邏輯：取得特定題目內容，若無則 404
    輸出：渲染 practice.html
    """
    pass

@practice_bp.route('/api/upload_audio', methods=['POST'])
def upload_audio():
    """
    處理錄音檔上傳與評分 (API)
    輸入：Form Data (audio_blob, topic_id)
    邏輯：
    1. 儲存暫存音檔
    2. 呼叫語音辨識 API 取得辨識文字
    3. 比對標準答案，計算分數與錯字
    4. 建立 Record 寫入資料庫
    5. 刪除暫存檔
    輸出：回傳 JSON 格式的分數與錯字陣列
    """
    pass
