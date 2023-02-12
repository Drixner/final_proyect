"""
inciando con fastapi con importaciones
"""
# Importa las clases StaticFiles y FastAPI desde el paquete fastapi,
# así como dos archivos de rutas llamados "products" y "users".
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users

# Crea una instancia de la clase FastAPI y la asigna a la variable "app".
app = FastAPI()

# Incluye dos routers en la aplicación FastAPI.
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)



# Monta una ruta estática para acceder a los archivos estáticos en la carpeta "static".
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define una ruta principal que devuelve el string "Hola Drixner!".
@app.get("/")
async def root():
    """
    devuele un string al iniciar en la ruta principal
    """
    return "Hola Drixner!"

# Define una ruta que devuelve un diccionario JSON con una URL.
@app.get("/url")
async def url():
    """
    devuele un json con una url
    """
    return {"url":"https://drixner.github.io/myportfolio/"}


