from fastapi import HTTPException
from model.database import Database, table # importa a classe Database do arquivo model/database.py
from app.create import get_id_by_name

db = Database()
tb = table()


db = Database()

 

@staticmethod
def update_item(table_name: str, nome: str, item: dict):
        if table_name not in tb.TABELAS:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        try:
            id_valor = get_id_by_name(table_name, nome)
            colunas = tb.TABELAS[table_name]
            chave_primaria = tb.PRIMARY_KEYS[table_name]

            set_clause = ', '.join([f"{col} = %s" for col in colunas])
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {chave_primaria} = %s"
            params = tuple(item[col] for col in colunas) + (id_valor,)

            with Database() as db:
                db.executar(sql, params)

            return {"message": "Item atualizado com sucesso!"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item: {str(e)}")
