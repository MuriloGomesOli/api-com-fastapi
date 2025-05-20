from fastapi import APIRouter
from model.database import Database, PRIMARY_KEYS # importa a classe Database do arquivo model/database.py
from app.update import update_item
from app.delete import delete_item
from app.create import create_item, criar_ator_serie
from app.read import gettotal, read_item
from model.database import Ator_serie

 
db = Database()
router = APIRouter()

 
@router.get("/{table_name}/{nome}")
def get_routes(table_name: str, nome: str = None):
    return read_item(table_name, nome)

@router.get('/{table_name}')
def get_total_routes(table_name: str, item_id: int = None):
    return gettotal(table_name, item_id)

@router.post("/ator_serie/completo")
def criar_personagem_router(ator: Ator_serie):
    return criar_ator_serie(ator)

@router.post("/{table_name}")
def create_routes(table_name: str, item: dict):
    return create_item(table_name, item)

@router.put("/{table_name}/{nome}")
def update_routes(table_name: str, nome: str, item: dict):
    return update_item(table_name, nome, item)

@router.delete("/{table_name}/{nome}")
def delete_routes(table_name: str, nome: str):
    return delete_item(table_name, nome)