"""
inicializa la aplicacion
"""
from fastapi import FastAPI
from routers import products

app = FastAPI()

# routers
app.include_router(products.router)

@app.get("/")
async def root():
    """
    es la ruta principal
    """
    return "Hola Drixner!"


@app.get("/url")
async def url():
    """
    Devuelve la url de mi portafolio
    """
    return {"url":"https://drixner.github.io/myportfolio/"}
