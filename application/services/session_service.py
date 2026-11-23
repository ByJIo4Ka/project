import datetime
from typing import Optional
import pymysql
from pymysql import Connection
from secrets import token_hex


class SessionService:
    def __init__(self, conn: Connection):
        self.conn = conn

    def create_session(self, user_id: int) -> Optional[str]:
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        session_id = token_hex(64)
        try:
            cursor.execute("""
            INSERT INTO users_sessions(user_session_id, user_id, expires_at)
                values (%s, %s, %s)
            """, (session_id, user_id, (datetime.datetime.now(datetime.timezone.utc)) + datetime.timedelta(days=1)))
            self.conn.commit()
            return session_id
        except Exception as e:
            self.conn.rollback()
            return None

    def get_user_by_session_id(self, session_id: str) -> Optional[dict]:
        query = """
        SELECT user_first_name as first_name,
               user_last_name as last_name,
               user_login as login,
               user_email as email,
               user_password_hash as password
        FROM users
        INNER JOIN users_sessions ON users.user_id = users_sessions.user_id
        where user_session_id = %s
        LIMIT 1
        """
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, (session_id,))
        result = cursor.fetchone()
        return None if result is None else result

    def check_session(self, session_id: str) -> Optional[str]:
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
        SELECT user_session_id, user_id, expires_at
        FROM users_sessions
            WHERE user_session_id = %s
            AND now() < expires_at
        """, (session_id, ))

        session = cursor.fetchone()
        return session["user_session_id"] if session else None

    def delete_session(self, session_id: str) -> str:
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
        DELETE FROM users_sessions
            WHERE user_session_id = %s
                       """, (session_id,))
        self.conn.commit()
        return session_id
