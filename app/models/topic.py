from app.models.db import get_db

class Topic:
    """口說題目資料操作模型"""
    
    @staticmethod
    def create(title, content, audio_path=None, difficulty='Normal'):
        """
        新增一筆口說題目
        :param title: 題目名稱
        :param content: 題目內容(英文)
        :param audio_path: 標準發音音檔路徑
        :param difficulty: 難易度
        :return: 新增的題目 ID 或 None
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO topics (title, content, audio_path, difficulty) VALUES (?, ?, ?, ?)",
                    (title, content, audio_path, difficulty)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating topic: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有題目
        :return: 題目紀錄列表
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM topics ORDER BY created_at DESC").fetchall()
        except Exception as e:
            print(f"Error getting all topics: {e}")
            return []

    @staticmethod
    def get_by_id(topic_id):
        """
        根據 ID 取得單筆題目
        :param topic_id: 題目 ID
        :return: 單筆紀錄或 None
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
        except Exception as e:
            print(f"Error getting topic by id: {e}")
            return None

    @staticmethod
    def update(topic_id, title, content, audio_path, difficulty):
        """
        更新題目資料
        :return: True 表示成功，False 表示失敗
        """
        try:
            with get_db() as conn:
                conn.execute(
                    "UPDATE topics SET title = ?, content = ?, audio_path = ?, difficulty = ? WHERE id = ?",
                    (title, content, audio_path, difficulty, topic_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating topic: {e}")
            return False

    @staticmethod
    def delete(topic_id):
        """
        刪除題目
        :param topic_id: 題目 ID
        :return: True 表示成功，False 表示失敗
        """
        try:
            with get_db() as conn:
                conn.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting topic: {e}")
            return False
