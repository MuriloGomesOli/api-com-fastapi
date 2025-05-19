from typing import Union # une duas informações
from fastapi import FastAPI, HTTPException
from model.database import Database, PRIMARY_KEYS # importa a classe Database do arquivo model/database.py
from app.update import update_item
from app.delete import delete_item
from app.create import create_item
from pydantic import BaseModel
 
app = FastAPI() # instancia a aplicação
db = Database()

class Ator_Personagem(BaseModel):

    nome_ator:str
    titulo: str
    personagem: str

 
@app.get('/') # define a rota raiz
def read_root():
    return {"Series": "Must Watch"} # retorna um dicionário com a mensagem "Must " -> json
 
@app.get("/{table_name}/{item_id}")
@app.get("/{table_name}")
def read_item(table_name: str, item_id: int = None):
    """
    Consulta uma tabela específica no banco de dados pelo ID.
    """
    db.conectar()  # Conecta ao banco de dados
 

 
    coluna_id = PRIMARY_KEYS.get(table_name)
 
    try:
        if item_id is None:
            sql = f"SELECT * FROM {table_name}"
            params = ()
        else:
            sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
            params = (item_id,)
 
        resultado = db.consultar(sql, params)
        db.desconectar()
       
        if not resultado:
            raise HTTPException(status_code=404, detail="Item não encontrado")
 
        return resultado
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
    
@app.post("/ator_serie/completo")
def criar_ator_serie(ator : Ator_Personagem):
 
    db = Database()
    db.conectar()
 
    query = f"Select id_autor from ator where (nome like '%{ator.nome_ator}%') limit 1"
    id_ator = db.select(query) #retorna uma lista de tuplas
    id_ator = id_ator[0]['id_autor']
 
    query = f"Select id_serie from serie where (titulo like '%{ator.titulo}%') limit 1"
    id_serie = db.select(query) #retorna uma lista de tuplas
    id_serie = id_serie[0]['id_serie']
 
 
 
    sql = "INSERT INTO ator_serie (id_serie, id_ator, personagem) VALUES (%s, %s,%s)"
    db.executar(sql,(id_serie,id_ator, ator.personagem))
    db.desconectar()
    return {"mensagem": "Série vinculada ao ator com sucesso"}
    
@app.post("/{table_name}")
def create_routes(table_name: str, item: dict):
    return create_item(table_name, item)

@app.put("/{table_name}/{item_id}")
def update_routes(table_name: str, item_id: int, item: dict):
    return update_item(table_name, item_id, item)

@app.delete("/{table_name}/{item_id}")
def delete_routes(table_name: str, item_id: int):
    return delete_item(table_name, item_id)