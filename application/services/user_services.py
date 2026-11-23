import argon2
import pymysql
from pymysql import Connection

class UserService:
    def __init__(self, conn: Connection):
        self.connection = conn
        self.PH = argon2.PasswordHasher()

    def get_user_by_id(self, user_id: int) -> dict:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute(
            """
            SELECT
                user_first_name as first_name,
                user_last_name as last_name,
                user_login as login,
                user_email as email,
                user_password_hash as password
            FROM users
            where user_id = %s
            """, (user_id,)
        )

        user = cursor.fetchone()
        cursor.close()
        return user

    def get_all_users(self) -> list:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

        cursor.execute(
            """
            SELECT
                user_first_name as first_name,
                user_last_name as last_name,
                user_login as login,
                user_email as email,
                user_password_hash as password
            FROM users
            """
        )

        users = cursor.fetchmany()
        cursor.close()
        return list(users)

    def create_user(self, first_name: str, last_name: str, login: str, email: str, password: str) -> dict:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        password = self.PH.hash(password)
        cursor.execute(
            """
            INSERT INTO users (user_first_name,
                               user_last_name,
                               user_login,
                               user_email,
                               user_password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, login, email, password)
        )
        self.connection.commit()
        cursor.execute(
            """
            SELECT user_first_name    as first_name,
                   user_last_name     as last_name,
                   user_login         as login,
                   user_email         as email,
                   user_password_hash as password
            FROM users
            where user_id = %s
            """, (cursor.lastrowid,)
        )
        user = cursor.fetchone()
        cursor.close()
        return user




    def update_user_full(self, user_id: int, first_name: str, last_name: str, login: str, email: str, password: str) -> dict | None:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            return None
        password_hash = self.PH.hash(password)
        cursor.execute(
            """
            UPDATE users SET user_first_name=%s, user_last_name=%s, user_login=%s, user_email=%s, user_password_hash=%s
            WHERE user_id=%s
            """, (first_name, last_name, login, email, password_hash, user_id)
        )
        self.connection.commit()
        cursor.execute(
            "SELECT user_first_name as first_name, user_last_name as last_name, user_login as login, user_email as email, user_password_hash as password FROM users WHERE user_id = %s",
            (user_id,)
        )
        updated_user = cursor.fetchone()
        cursor.close()
        return updated_user

    def update_user_partial(self, user_id: int, data: dict) -> dict | None:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            return None
        field_map = {
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "login": "user_login",
            "email": "user_email",
            "password": "user_password_hash",
        }
        set_clauses, values = [], []
        for key, value in data.items():
            if key in field_map and value is not None:
                if key == "password":
                    value = self.PH.hash(value)
                set_clauses.append(f"{field_map[key]} = %s")
                values.append(value)
        if set_clauses:
            values.append(user_id)
            cursor.execute(f"UPDATE users SET {', '.join(set_clauses)} WHERE user_id = %s", tuple(values))
            self.connection.commit()
        cursor.execute(
            "SELECT user_first_name as first_name, user_last_name as last_name, user_login as login, user_email as email, user_password_hash as password FROM users WHERE user_id = %s",
            (user_id,)
        )
        updated_user = cursor.fetchone()
        cursor.close()
        return updated_user

    def delete_user(self, user_id: int) -> bool:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            return False
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        self.connection.commit()
        cursor.close()
        return True