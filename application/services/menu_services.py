from typing import Optional
import pymysql
from pymysql import Connection

class MenuService:
    def __init__(self, conn: Connection):
        self.connection = conn

    def get_menu_item_by_id(self, item_id: int) -> Optional[dict]:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM menu_items WHERE menu_item_id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        return item

    def get_all_menu_items(self) -> list:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM menu_items ORDER BY menu_item_order ASC, menu_item_id ASC")
        items = cursor.fetchall()
        cursor.close()
        return list(items)

    def create_menu_item(self, data: dict) -> Optional[dict]:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(
            """INSERT INTO menu_items (menu_item_name, menu_item_link, menu_item_order, menu_item_parent_id, icon_name, menu_item_is_hidden, menu_item_description, menu_item_sidebar_hidden)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (data.get("menu_item_name"), data.get("menu_item_link"), data.get("menu_item_order"), data.get("menu_item_parent_id"),
             data.get("icon_name"), data.get("menu_item_is_hidden", 0), data.get("menu_item_description"), data.get("menu_item_sidebar_hidden", 0))
        )
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return self.get_menu_item_by_id(new_id)

    def update_menu_item(self, item_id: int, fields: dict) -> Optional[dict]:
        if not fields:
            return self.get_menu_item_by_id(item_id)
        set_clauses = [f"{key} = %s" for key in fields.keys()]
        values = list(fields.values()) + [item_id]
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(f"UPDATE menu_items SET {', '.join(set_clauses)} WHERE menu_item_id = %s", tuple(values))
        self.connection.commit()
        cursor.close()
        return self.get_menu_item_by_id(item_id)

    def delete_menu_item(self, item_id: int) -> bool:
        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM menu_items WHERE menu_item_id = %s", (item_id,))
        self.connection.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        return deleted
