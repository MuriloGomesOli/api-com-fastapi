from typing import Union # une duas informações
from fastapi import FastAPI, HTTPException
from model.database import Database # importa a classe Database do arquivo model/database.py
from app.update import update_item
from app.delete import delete_item
from app.create import create_item
 
app = FastAPI() # instancia a aplicação
db = Database()
 
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
 
    tabelas_permitidas = {
    'serie': 'id_serie',
    'categoria': 'id_categoria',
    'ator': 'id_ator',
    'motivo_assistir': 'id_motivo',
}

 
    coluna_id = tabelas_permitidas.get(table_name)
 
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
    
@app.post("/{table_name}")
def create_routes(table_name: str, item: dict):
    return create_item(table_name, item)

@app.put("/{table_name}/{item_id}")
def update_routes(table_name: str, item_id: int, item: dict):
    return update_item(table_name, item_id, item)

@app.delete("/{table_name}/{item_id}")
def delete_routes(table_name: str, item_id: int):
    return delete_item(table_name, item_id)