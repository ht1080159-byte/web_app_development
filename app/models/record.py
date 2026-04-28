from app.models.db import get_db
import json

class Record:
    @staticmethod
    def create(user_id, topic_id, score, wrong_words):
        wrong_words_json = json.dumps(wrong_words)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO records (user_id, topic_id, score, wrong_words) VALUES (?, ?, ?, ?)",
                (user_id, topic_id, score, wrong_words_json)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_user(user_id):
        with get_db() as conn:
            return conn.execute(
                "SELECT records.*, topics.title as topic_title FROM records "
                "JOIN topics ON records.topic_id = topics.id "
                "WHERE user_id = ? ORDER BY records.created_at DESC", 
                (user_id,)
            ).fetchall()
