from typing import Union # une duas informações
from fastapi import FastAPI, HTTPException
from model.database import Database # importa a classe Database do arquivo model/database.py
 
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
def create_item(table_name: str, item: dict):
    '''Adiciona um item a uma tabela específica no banco de dados'''
    db.conectar()
 
    try:
        if table_name == 'serie':
            sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (?, ?, ?, ?)"
            params = (item['titulo'], item['descricao'], item['ano_lancamento'], item['id_categoria'])
        elif table_name == 'categoria':
            sql = "INSERT INTO categoria (categoria_nome) VALUES (?)"
            params = (item['categoria_nome'],)
        elif table_name == 'ator':
            sql = "INSERT INTO ator (nome) VALUES (?)"
            params = (item['nome'],)
        elif table_name == 'motivo_assistir':
            sql = "INSERT INTO motivo_assistir (id_serie, motivo) VALUES (?, ?)"
            params = (item['id_serie'], item['motivo'])
        else:
            raise HTTPException(status_code=400, detail="Tabela não permitida")
 
        db.executar(sql, params)
        db.desconectar()
 
        return {"message": "Item adicionado com sucesso!"}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar o item: {str(e)}")