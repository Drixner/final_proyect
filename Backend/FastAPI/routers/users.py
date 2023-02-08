"""
importacion del modulo fastAPI
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
        tags=["users"]
        )

# Inicia el server: uvicorn users:router --reload

# Entidad user
class User(BaseModel):
    """
    la clase User usada para definir todas las varibles y a su vez, formateadas
    """
    id: int
    name: str
    surname: str
    url: str
    age: int

# Lista de usuarios
users_list = [User(id=1, name="Drixner", surname="Condor",
            url="https://drixner.github.io/myportfolio/", age=30),
            User(id=2, name="Yngrid", surname="Barrera", url="google.com", age=24),
            User(id=3, name="Kattie", surname="Condor", url="maps.com", age=24)]


@router.get("/usersjson")
async def users_json():
    """
    Devuelve la lista de usuarios en formato JSON
    """
    return [
        {
            "name": "Drixner",
            "surname": "Condor",
            "url": "https://drixner.github.io/myportfolio/",
            "age": 30
        },
        {
            "name": "Yngrid",
            "surname": "Barrera",
            "url": "https://drixner.github.io/myportfolio/",
            "age": 23
        },
        {
            "name": "Kattie",
            "surname": "Condor",
            "url": "https://drixner.github.io/myportfolio/",
            "age": 26
        }
    ]


@router.get("/users")
async def users():
    """
    Devuelve la lista de usuarios
    """
    return users_list

#path
@router.get("/user/{id}")
async def user_list(id: int):
    """
    Devuelve un usuario por su id
    """
    return search_user(id)


#query
@router.get("/user/")
async def user(id: int):
    """
    Devuelve un usuario por su id
    """
    return search_user(id)


#METODO POST insertar valores
@router.post("/user/",response_model=User, status_code=201)
async def join_user(user: User):
    """
    Crea un nuevo usuario
    """
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    users_list.append(user)
    return user


#   METODO PUT
@router.put("/user/")
async def update_user(user: User):
    """
    Actualiza un usuario existente
    """

    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {'error': 'No se ha actualizado el usuario'}
    return user


# METODO DELETE
@router.delete("/user/{id}")
async def delete_user(id: int):
    """
    Elimina un usuario existente
    """
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {'error': 'No se ha eliminado el usuario'}
# <-- Check

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}
