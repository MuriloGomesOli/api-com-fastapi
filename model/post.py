from typing import Union 
from fastapi import FastAPI, HTTPException
from model.database import Database as db
from app.main import FastAPI as app

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