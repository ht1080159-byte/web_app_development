from app.models.db import get_db

class User:
    @staticmethod
    def create(username, email, password_hash):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(user_id):
        with get_db() as conn:
            return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    @staticmethod
    def get_by_email(email):
        with get_db() as conn:
            return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
