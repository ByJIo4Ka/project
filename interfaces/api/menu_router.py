from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pymysql import Connection
from application.services.menu_services import MenuService
from infrastructure.db.mySQL import mysql_conn

router = APIRouter(prefix="/menu", tags=["menu"])

class MenuItemCreate(BaseModel):
    menu_item_name: str
    menu_item_link: Optional[str] = None
    menu_item_order: Optional[int] = 0
    menu_item_parent_id: Optional[int] = None
    icon_name: Optional[str] = None
    menu_item_is_hidden: Optional[int] = 0
    menu_item_description: Optional[str] = None
    menu_item_sidebar_hidden: Optional[int] = 0

class MenuItemUpdate(BaseModel):
    menu_item_name: Optional[str] = None
    menu_item_link: Optional[str] = None
    menu_item_order: Optional[int] = None
    menu_item_parent_id: Optional[int] = None
    icon_name: Optional[str] = None
    menu_item_is_hidden: Optional[int] = None
    menu_item_description: Optional[str] = None
    menu_item_sidebar_hidden: Optional[int] = None

@router.get("/get_menu_items", summary="Получение всех пунктов меню")
async def get_menu_items(conn: Connection = Depends(mysql_conn)):
    return {"menu_items": MenuService(conn).get_all_menu_items()}

@router.post("/create_menu_item", summary="Добавление пункта меню")
async def create_menu_item(item: MenuItemCreate, conn: Connection = Depends(mysql_conn)):
    created = MenuService(conn).create_menu_item(item.model_dump())
    if created is None:
        raise HTTPException(status_code=500, detail="Failed to create menu item")
    return created

@router.put("/{menu_item_id}", summary="Полное обновление пункта меню")
async def update_menu_item_put(menu_item_id: int, item: MenuItemCreate, conn: Connection = Depends(mysql_conn)):
    updated = MenuService(conn).update_menu_item(menu_item_id, item.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated

@router.patch("/{menu_item_id}", summary="Частичное обновление пункта меню")
async def update_menu_item_patch(menu_item_id: int, item: MenuItemUpdate, conn: Connection = Depends(mysql_conn)):
    updated = MenuService(conn).update_menu_item(menu_item_id, item.model_dump(exclude_unset=True))
    if updated is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated

@router.delete("/{menu_item_id}", summary="Удаление пункта меню")
async def delete_menu_item(menu_item_id: int, conn: Connection = Depends(mysql_conn)):
    if not MenuService(conn).delete_menu_item(menu_item_id):
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"detail": f"Menu item {menu_item_id} successfully deleted"}
