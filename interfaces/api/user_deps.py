from fastapi import Cookie, HTTPException

from infrastructure.db.mySQL import get_async_conn
from application.services.session_service import SessionService


def check_session(session_id: str | None = Cookie(default=None, alias="session_id")) -> str:
    if session_id is None:
        raise HTTPException(status_code=401, detail="user is not logged in")

    with get_async_conn() as conn:
        if SessionService(conn).check_session(session_id):
            return session_id
        else:
            raise HTTPException(status_code=401, detail="invalid session_id")
