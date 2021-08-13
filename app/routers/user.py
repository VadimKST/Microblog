from fastapi import APIRouter, Form
from passlib.context import CryptContext

from core.models.model import user, user_details
from core.schemas.schemes import RegisterUser
from db import connection

router = APIRouter(prefix="/user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}


@router.post("/register")
def register(data_user: RegisterUser):
    hash_password = get_password_hash(data_user.password)
    query_user = user.insert().values(
        username=data_user.username,
        email=data_user.email,
        password=hash_password
    )
    print(query_user)
    connection.execute(query_user)
    data_new_user = connection.execute(user.select().where(user.c.username == data_user.username))
    query_user_details = user_details.insert().values(
        user_id=data_new_user.first().id,
        name=data_user.name,
        surname=data_user.surname,
        patronymic=data_user.patronymic,
        city=data_user.city,
        age=data_user.age,
        about_me=data_user.about_me
    )
    print(query_user_details)
    connection.execute(query_user_details)
    return data_user

