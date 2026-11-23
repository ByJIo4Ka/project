import pymysql
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="admin",  # <-- впишите ваш пароль
    charset="utf8mb4",
    autocommit=True
)

try:
    with connection.cursor() as cursor:
        # 1. Создаем базу данных, если она еще не создана
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS primer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        print("База данных primer_db успешно создана!")

        # 2. Переключаемся на созданную базу данных
        cursor.execute("USE primer_db;")

        # 3. Создаем таблицу users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id serial primary key,
                user_first_name varchar(255) not null,
                user_last_name varchar(255) not null,
                user_login varchar(255) not null,
                user_email varchar(255) not null,
                user_password_hash varchar(255) not null
            );
        """)
        print("Таблица users успешно создана!")
finally:
    connection.close()