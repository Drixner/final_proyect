"""
modudule of producto
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def products():
    """
    Devuelve la lista de productos
    """
    return ["producto1", "producto2", "producto3","producto4", "producto5", "producto6"]
