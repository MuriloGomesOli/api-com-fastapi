from fastapi import HTTPException
from model.database import Database, table # importa a classe Database do arquivo model/database.py
from app.create import get_id_by_name

db = Database()
tb = table()



@staticmethod
def gettotal(table_name: str, item_id: int = None):
        coluna_id = tb.PRIMARY_KEYS.get(table_name)
        if not coluna_id:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        try:
            with Database() as db:
                if item_id is None:
                    sql = f"SELECT * FROM {table_name}"
                    params = ()
                else:
                    sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
                    params = (item_id,)

                resultado = db.consultar(sql, params)

                if not resultado:
                    raise HTTPException(status_code=404, detail="Item não encontrado")

                return resultado

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
 
@staticmethod
def read_item(table_name: str, nome: str):
        try:
            id_valor = get_id_by_name(table_name, nome)
            coluna_id = tb.PRIMARY_KEYS[table_name]

            with Database() as db:
                sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
                resultado = db.consultar(sql, (id_valor,))

                if not resultado:
                    raise HTTPException(status_code=404, detail="Item não encontrado")

                return resultado

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
