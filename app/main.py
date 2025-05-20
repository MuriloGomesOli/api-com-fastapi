from typing import Union 
from fastapi import FastAPI
from model.database import Database, PRIMARY_KEYS
from routes import serie
 
app = FastAPI() # instancia a aplicação
db = Database()

app.include_router(serie.router)
 
@app.get('/') # define a rota raiz
def read_root():
    return {"Series": "Must Watch"} # retorna um dicionário com a mensagem "Must " -> json