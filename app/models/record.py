from app.models.db import get_db
import json

class Record:
    """使用者測驗紀錄資料操作模型"""
    
    @staticmethod
    def create(user_id, topic_id, score, wrong_words):
        """
        新增一筆測驗紀錄
        :param user_id: 使用者 ID
        :param topic_id: 題目 ID
        :param score: 分數
        :param wrong_words: 錯字陣列 (將被轉為 JSON)
        :return: 新增的紀錄 ID 或 None
        """
        try:
            wrong_words_json = json.dumps(wrong_words)
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO records (user_id, topic_id, score, wrong_words) VALUES (?, ?, ?, ?)",
                    (user_id, topic_id, score, wrong_words_json)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating record: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有紀錄
        :return: 紀錄列表
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM records ORDER BY created_at DESC").fetchall()
        except Exception as e:
            print(f"Error getting all records: {e}")
            return []

    @staticmethod
    def get_by_id(record_id):
        """
        根據 ID 取得單筆紀錄
        :param record_id: 紀錄 ID
        :return: 單筆紀錄或 None
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
        except Exception as e:
            print(f"Error getting record by id: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        """
        取得特定使用者的所有紀錄 (並附帶題目名稱)
        :param user_id: 使用者 ID
        :return: 該使用者的紀錄列表
        """
        try:
            with get_db() as conn:
                return conn.execute(
                    "SELECT records.*, topics.title as topic_title FROM records "
                    "JOIN topics ON records.topic_id = topics.id "
                    "WHERE user_id = ? ORDER BY records.created_at DESC", 
                    (user_id,)
                ).fetchall()
        except Exception as e:
            print(f"Error getting records by user: {e}")
            return []

    @staticmethod
    def update(record_id, score, wrong_words):
        """
        更新紀錄
        :return: True 表示成功，False 表示失敗
        """
        try:
            wrong_words_json = json.dumps(wrong_words)
            with get_db() as conn:
                conn.execute(
                    "UPDATE records SET score = ?, wrong_words = ? WHERE id = ?",
                    (score, wrong_words_json, record_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    @staticmethod
    def delete(record_id):
        """
        刪除紀錄
        :param record_id: 紀錄 ID
        :return: True 表示成功，False 表示失敗
        """
        try:
            with get_db() as conn:
                conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
