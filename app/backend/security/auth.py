from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Response, Form
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter()

fake_users_db = {
    "Irina": {
        "username": "Irina",
        "password": "Irina_Mishariki_17.04.2025",
    }
}

active_sessions = {}


# Эндпоинты
@router.post("/login")
async def login(
        response: Response,
        username: str = Form(),
        password: str = Form()
):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль",
        )
    # Создаем сессию
    session_token = str(uuid4())
    active_sessions[session_token] = username

    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="session_token", value=session_token, httponly=True, max_age=18000)
    return response


@router.get("/protected")
async def protected_page(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in active_sessions:
        return False
    username = active_sessions[session_token]
    if username != "Irina":
        return False
    return True
