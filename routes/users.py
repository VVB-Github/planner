#-----------------------------Импорты-------------------------------
from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn
from fastapi.templating import Jinja2Templates

# Класс Request в FastAPI дает информацию о входящем HTTP-запросе
from fastapi import Request

# позволяет нам возвращать HTML-страницы
from fastapi.responses import HTMLResponse

#----------------------------Настройки роутера--------------------------
# указываем строку где находятся темплейты
templates = Jinja2Templates(directory="templates")
# Создаем роутер
user_router = APIRouter(
    tags=["User"],
)
# получаем обьект для работы с БД
user_database = Database(User)
#---------------------------Маршруты------------------------------

# Путь подписи юзера
@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists already"
        )
    await user_database.save(user)
    return {
        "message": "User created successfully"
    }

# Путь входа пользователей
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    if user_exist.password == user.password:
        return {
            "message": "User signed in successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

