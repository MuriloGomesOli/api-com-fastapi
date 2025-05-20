from fastapi import HTTPException
from model.database import Database, PRIMARY_KEYS # importa a classe Database do arquivo model/database.py
 
db = Database()


def delete_item(table_name: str, nome: str):
        '''Remove um item de uma tabela específica no banco de dados'''
        db.conectar()
        def teste():
            if table_name == "serie":
                resultado = "titulo"
            elif table_name == "categoria":
                resultado = "nome_categoria"
            elif table_name == "ator":
                resultado = "nome"
            else:
                resultado = None
            return resultado
        
        coluna = teste()

        try:
            if table_name not in PRIMARY_KEYS:
                raise HTTPException(status_code=400, detail="Tabela não permitida")
            
            query = f"SELECT {PRIMARY_KEYS[table_name]} FROM {table_name} WHERE {coluna} LIKE '%{nome}%' LIMIT 1"
            resultado = db.select(query)
            id_valor = resultado[0][PRIMARY_KEYS[table_name]]  

            chave_primaria = PRIMARY_KEYS[table_name]
            sql = f"DELETE FROM {table_name} WHERE {chave_primaria} = %s"

            db.executar(sql, (id_valor,))
            db.desconectar()

            return {"message": "Item removido com sucesso!"}

        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao remover o item: {str(e)}")