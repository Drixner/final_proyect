"""
modudule of producto
"""
from fastapi import APIRouter



router = APIRouter(prefix="/products",
                tags=["products"],# se utiliza para la documentacion
                responses={404: {"messages": "No encontrado"}})

products_list = [
        "producto0", "producto2", "producto3","producto4", "producto5", "producto6"
        ]

@router.get("")
async def products():
    """
    Devuelve la lista de productos
    """
    return products_list


@router.get("/{id}")
async def products_id(id: int):
    """
    Devuelve la lista de productos
    """
    return products_list[id]
