"""
inicializacion de la autenticacion basica
"""
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel

router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    """
    Clase para el usuario
    """
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    """
    Clase para la base de datos de usuarios, que vela por la contrasena
    """
    password: str


users_db = {
    "drixner": {
        "username" : "drixner",
        "full_name" : "Drixner Condor",
        "email" : "drixner@gmail.com",
        "disabled": False,
        "password": "123drix",
    },

    "Yngrid": {
        "username" : "yngrid",
        "full_name" : "Yngrid Barrera",
        "email" : "titi@gmail.com",
        "disabled": True,
        "password": "123titi",
    }
}

def search_user_db(username: str):
    """
    para la busqueda del usuario
    """
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    """
    para la busqueda del usuario
    """
    if username in users_db:
        return User(**users_db[username])



async def current_user(token: str = Depends(oauth2)):
    """
    funcion para el usuario actual
    """
    user = search_user(token)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de autorizacion invalidas",
                headers={"WWW-authenticate":"bearer"})

    if user.disabled:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario deshabilitado")
    return user




@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    funcion para autenticar al usuario
    """
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correctdo")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}




@router.get("/users/me")
async def read_users_me(user: User = Depends(current_user)):
    """
    funcion para leer el usuario
    """
    return user



