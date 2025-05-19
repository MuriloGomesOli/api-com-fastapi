from fastapi import HTTPException
from model.database import Database, TABELAS, PRIMARY_KEYS

db = Database()

 

def update_item(table_name: str, item_id: int, item: dict):
    db.conectar()

    try:
        if table_name not in TABELAS:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        colunas = TABELAS[table_name]
        chave_primaria = PRIMARY_KEYS[table_name]

        set_clause = ', '.join([f"{col} = %s" for col in colunas])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {chave_primaria} = %s"

        params = tuple(item[col] for col in colunas) + (item_id,)

        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item atualizado com sucesso!"}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item: {str(e)}")
