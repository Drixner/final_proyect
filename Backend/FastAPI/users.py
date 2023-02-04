"importacion del modulo fastAPI"
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# inicia el server: uvicorn users:app --reload
# entidad user

class User(BaseModel):
    " la clase User usada para definir todas las varibles y estas a la vez estan formateadas"
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Drixner", surname="Condor",
            url="https://drixner.github.io/myportfolio/", age=30),
            User(id=2, name="Yngrid", surname="Barrera", url="google.com", age=24),
            User(id=3, name="Kattie", surname="Condor", url="maps.com", age=24)]

#users_list = [User(name="Brais", surname="Moure", url="https://moure.dev", age=35),
#              User(name="Moure", surname="Dev",
#                   url="https://mouredev.com", age=35),
#              User(name="Brais", surname="Dahlberg", url="https://haakon.com", age=33)]

@app.get("/usersjson")
async def usersjson():
    "--Esto es una base de datos provicional--"

    return [{"name":"Drixner", "surname": "Condor",
            "url": "https://drixner.github.io/myportfolio/", "age": 30},
            {"name":"Yngrid", "surname": "Barrera",
            "url": "https://drixner.github.io/myportfolio/", "age": 23},
            {"name":"Kattie", "surname": "Condor",
            "url": "https://drixner.github.io/myportfolio/", "age": 26}]


@app.get("/users")
async def users():
    "--el portal para consultar lista de usuarios--"
    return users_list

#path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


#query
@app.get("/user/")
async def user(id: int):
    return search_user(id)


#   METODO POST insertar valores
@app.post("/user/", status_code=201)
async def user(user: User):
    if isinstance(search_user(user.id)) == User:
        HTTPException(status_code=204, detail="El usuario ya existe")
        return {"Error":"El usuario ya existe"}

    users_list.append(user)
    return user


#   METODO PUT
@app.put("/user/")
async def user(user:User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {'error': 'No se ha actualizado el usuario'}
    return user


# METODO DELETE
@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {'error': 'No se ha eliminado el usuario'}
# <-- Check


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}
