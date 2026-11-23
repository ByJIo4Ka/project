from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pymysql import Connection

from application.services.user_services import UserService
from infrastructure.db.mySQL import mysql_conn

router = APIRouter(prefix="/user", tags=["user"])


class User(BaseModel):
    first_name: str
    last_name: str
    login: str
    email: str
    password: str


class UserUpdatePatch(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    login: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


@router.get("/get_user_by_id/{user_id}")
async def get_user(user_id: int, conn: Connection = Depends(mysql_conn)):
    service = UserService(conn)
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/get_users")
async def get_users(
    limit: Optional[int] = 10,
    page: Optional[int] = 1,
    conn: Connection = Depends(mysql_conn)
):
    service = UserService(conn)
    users = service.get_all_users()
    return {
        "users": users,
        "page": page,
        "limit": limit
    }


@router.post(
    "/create_user",
    summary="Создаёт пользователя",
    description="Эндпоинт который создаёт нового пользователя",
    status_code=200,
    response_model=User
)
async def create_user(user: User, conn: Connection = Depends(mysql_conn)) -> Optional[User]:
    service = UserService(conn)
    created_user = service.create_user(
        user.first_name, user.last_name, user.login, user.email, user.password
    )
    return User(**created_user)


@router.put("/{user_id}", response_model=User, summary="Полное обновление пользователя")
async def update_user_put(user_id: int, user: User, conn: Connection = Depends(mysql_conn)):
    service = UserService(conn)
    updated_user = service.update_user_full(
        user_id, user.first_name, user.last_name, user.login, user.email, user.password
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**updated_user)


@router.patch("/{user_id}", response_model=User, summary="Частичное обновление пользователя")
async def update_user_patch(user_id: int, user_data: UserUpdatePatch, conn: Connection = Depends(mysql_conn)):
    service = UserService(conn)
    fields = user_data.model_dump(exclude_unset=True)
    updated_user = service.update_user_partial(user_id, fields)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**updated_user)


@router.delete("/{user_id}", summary="Удаление пользователя")
async def delete_user(user_id: int, conn: Connection = Depends(mysql_conn)):
    service = UserService(conn)
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User {user_id} successfully deleted"}
