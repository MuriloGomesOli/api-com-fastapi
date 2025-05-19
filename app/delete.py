from fastapi import HTTPException
from model.database import Database,PRIMARY_KEYS # importa a classe Database do arquivo model/database.py
 
db = Database()


def delete_item(table_name: str, item_id: int):
    '''Remove um item de uma tabela específica no banco de dados'''
    db.conectar()

    try:
        if table_name not in PRIMARY_KEYS:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        chave_primaria = PRIMARY_KEYS[table_name]
        sql = f"DELETE FROM {table_name} WHERE {chave_primaria} = %s"

        db.executar(sql, (item_id,))
        db.desconectar()

        return {"message": "Item removido com sucesso!"}

    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao remover o item: {str(e)}")