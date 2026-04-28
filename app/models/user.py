from app.models.db import get_db

class User:
    """使用者資料操作模型"""
    
    @staticmethod
    def create(username, email, password_hash):
        """
        新增一位使用者
        :param username: 使用者名稱
        :param email: 電子郵件
        :param password_hash: 雜湊後的密碼
        :return: 新增的使用者 ID 或 None (若發生錯誤)
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有使用者
        :return: 使用者紀錄列表 (sqlite3.Row)
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM users").fetchall()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """
        根據 ID 取得單筆使用者資料
        :param user_id: 使用者 ID
        :return: 單筆紀錄或 None
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """
        根據 Email 取得單筆使用者資料
        :param email: 電子郵件
        :return: 單筆紀錄或 None
        """
        try:
            with get_db() as conn:
                return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    @staticmethod
    def update(user_id, username, email):
        """
        更新使用者資料
        :param user_id: 使用者 ID
        :param username: 新的使用者名稱
        :param email: 新的電子郵件
        :return: True 表示成功，False 表示失敗
        """
        try:
            with get_db() as conn:
                conn.execute(
                    "UPDATE users SET username = ?, email = ? WHERE id = ?",
                    (username, email, user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """
        刪除使用者
        :param user_id: 使用者 ID
        :return: True 表示成功，False 表示失敗
        """
        try:
            with get_db() as conn:
                conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
