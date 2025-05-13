from typing import Union # une duas informações
from fastapi import FastAPI, HTTPException
from model.database import Database # importa a classe Database do arquivo model/database.py
 
app = FastAPI() # instancia a aplicação
db = Database()


def criar_serie(db, titulo, descricao, ano_lancamento, id_categoria):
    sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s)"
    Database.executar(sql, (titulo, descricao, ano_lancamento, id_categoria))

def listar_series(db):
    return Database.consultar("SELECT * FROM serie")

def buscar_serie_por_id(db, id_serie):
    return Database.consultar("SELECT * FROM serie WHERE id_serie = %s", (id_serie,))

