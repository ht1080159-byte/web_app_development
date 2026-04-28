from app.models.db import get_db

class Topic:
    @staticmethod
    def create(title, content, audio_path=None, difficulty='Normal'):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO topics (title, content, audio_path, difficulty) VALUES (?, ?, ?, ?)",
                (title, content, audio_path, difficulty)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            return conn.execute("SELECT * FROM topics ORDER BY created_at DESC").fetchall()

    @staticmethod
    def get_by_id(topic_id):
        with get_db() as conn:
            return conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
