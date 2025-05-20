from fastapi import HTTPException
from model.database import Database, PRIMARY_KEYS # importa a classe Database do arquivo model/database.py

db = Database()



def gettotal(table_name: str, item_id: int = None):
        """
        Consulta uma tabela específica no banco de dados pelo ID.
        """
        db.conectar()  # Conecta ao banco de dados
    
        tabelas_permitidas = {
        'serie': 'id_serie',
        'categoria': 'id_categoria',
        'ator': 'id_ator',
        'motivo_assistir': 'id_motivo',
    }

    
        coluna_id = tabelas_permitidas.get(table_name)
    
        try:
            if item_id is None:
                sql = f"SELECT * FROM {table_name}"
                params = ()
            else:
                sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
                params = (item_id,)
    
            resultado = db.consultar(sql, params)
            db.desconectar()
        
            if not resultado:
                raise HTTPException(status_code=404, detail="Item não encontrado")
    
            return resultado
        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")

 
def read_item(table_name: str, nome: str):
        """
        Consulta uma tabela específica no banco de dados pelo ID.
        """
        db.conectar()  # Conecta ao banco de dados
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
    
        tabelas_permitidas = {
        'serie': 'id_serie',
        'categoria': 'id_categoria',
        'ator': 'id_ator',
        'motivo_assistir': 'id_motivo',
    }
        query = f"SELECT {PRIMARY_KEYS[table_name]} FROM {table_name} WHERE {coluna} LIKE '%{nome}%' LIMIT 1"
        resultado = db.select(query)
        id_valor = resultado[0][PRIMARY_KEYS[table_name]] 
        

    
        coluna_id = tabelas_permitidas.get(table_name)
    
        try:
            if id_valor is None:
                sql = f"SELECT * FROM {table_name}"
                params = ()
            else:
                sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
                params = (id_valor,)
    
            resultado = db.consultar(sql, params)
            db.desconectar()
        
            if not resultado:
                raise HTTPException(status_code=404, detail="Item não encontrado")
    
            return resultado
        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")