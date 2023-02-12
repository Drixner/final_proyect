"""
inicializacion de la autenticacion basica
"""
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"  #algoritmo de encriptacion
ACCESS_TOKEN_EXPIRE_MINUTES = 1  #tiempo de expiracion del token
SECRET="13d6c7dc98ffcb88114e8b72401b6b03dd96a151346b1a71c90a24d97e603095"  #clave secreta

router = APIRouter()  #inicializacion del router

oauth2 = OAuth2PasswordBearer(tokenUrl="login")  #inicializacion de la autenticacion basica
 
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #inicializacion de la encriptacion

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
        "password": "$2a$12$7m69MFJTcO3YGuJomhrk7OP5k8qE5bo3CJpHlrlyv/IRhIFV0YczS",
    },

    "Yngrid": {
        "username" : "yngrid",
        "full_name" : "Yngrid Barrera",
        "email" : "titi@gmail.com",
        "disabled": True,
        "password": "$2a$12$INAWqVuTvEzJIhBRbl.KROThkwPhwpZBHp/RAx7E.Dl88Lg8/I9/e",
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
        return UserDB(**users_db[username])




async def auth_user(token: str = Depends(oauth2)):

    exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autorizacion invalidas",
            headers={"WWW-authenticate":"bearer"}
            )


    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exceptions



    except JWTError:
        raise exceptions


    return search_user(username)


async def current_user(user : User = Depends(auth_user)):
    """
    funcion para el usuario actual
    """
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


    if not crypt_context.verify(form.password, user.password):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")


    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}

    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(user: User = Depends(current_user)):
    """
    funcion para leer el usuario
    """
    return user
