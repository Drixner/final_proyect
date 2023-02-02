from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# inicia el server: uvicorn users:app --reload
# entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Drixner", surname="Condor", url="https://drixner.github.io/myportfolio/", age=30),
              User(id=2, name="Yngrid", surname="Barrera", url="google.com", age=24),
              User(id=3, name="Kattie", surname="Condor", url="maps.com", age=24)]

#users_list = [User(name="Brais", surname="Moure", url="https://moure.dev", age=35),
#              User(name="Moure", surname="Dev",
#                   url="https://mouredev.com", age=35),
#              User(name="Brais", surname="Dahlberg", url="https://haakon.com", age=33)]

@app.get("/usersjson")
async def usersjson():
    return [{"name":"Drixner", "surname": "Condor", "url": "https://drixner.github.io/myportfolio/", "age": 30},
            {"name":"Yngrid", "surname": "Barrera", "url": "https://drixner.github.io/myportfolio/", "age": 23},
            {"name":"Kattie", "surname": "Condor", "url": "https://drixner.github.io/myportfolio/", "age": 26}]


@app.get("/users")
async def users():
    return users_list

#path
@app.get("/user/{id}")
async def user(id: int, name: str):
    return search_user(id)


#query
@app.get("/user/")
async def user(id: int):
    return search_user(id)


@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"Error":"El usuario ya existe"}
    else:
        users_list.append(user)


@app.put("/user/")
async def user():



def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"no se ha encontrado el usuario"}
