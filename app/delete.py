from fastapi import HTTPException
from model.database import Database, table # importa a classe Database do arquivo model/database.py
from app.create import get_id_by_name

db = Database()
tb = table()

db = Database()


@staticmethod
def delete_item(table_name: str, nome: str):
        if table_name not in tb.PRIMARY_KEYS:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        try:
            id_valor = get_id_by_name(table_name, nome)
            chave_primaria = tb.PRIMARY_KEYS[table_name]
            sql = f"DELETE FROM {table_name} WHERE {chave_primaria} = %s"

            with Database() as db:
                db.executar(sql, (id_valor,))

            return {"message": "Item removido com sucesso!"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao remover o item: {str(e)}")