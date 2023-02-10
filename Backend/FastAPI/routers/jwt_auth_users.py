"""
inicializacion de la autenticacion basica
"""
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI,Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt
from paslib.context import CryptContext


ALGORITHM = "HS256"  #algoritmo de encriptacion

app = FastAPI()  #inicializacion de la aplicacion

oauth2 = OAuth2PasswordBearer(tokenUrl="login")  #inicializacion de la autenticacion basica

crypt = 


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




@app.post("/login")
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
