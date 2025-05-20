from fastapi import HTTPException
from model.database import Database, TABELAS, PRIMARY_KEYS

db = Database()

 

def update_item(table_name: str,nome: str, item: dict):
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
            if table_name not in TABELAS:
                raise HTTPException(status_code=400, detail="Tabela não permitida")
                
            query = f"SELECT {PRIMARY_KEYS[table_name]} FROM {table_name} WHERE {coluna} LIKE '%{nome}%' LIMIT 1"
            resultado = db.select(query)
            id_valor = resultado[0][PRIMARY_KEYS[table_name]]    

            colunas = TABELAS[table_name]
            chave_primaria = PRIMARY_KEYS[table_name]

            set_clause = ', '.join([f"{col} = %s" for col in colunas])
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {chave_primaria} = %s"

            params = tuple(item[col] for col in colunas) + (id_valor,)

            db.executar(sql, params)
            db.desconectar()

            return {"message": "Item atualizado com sucesso!"}
        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item: {str(e)}")
