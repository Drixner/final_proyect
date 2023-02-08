from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


users_db = {
    "drixner": {
        "username" : "drixner",
        "full_name" : "Drixner Condor",
        "email" : "drixner@gmail.com",
        "disabled": False,
        "password": "123drix",
        }
    }
