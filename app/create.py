from fastapi import HTTPException
from model.database import Database # importa a classe Database do arquivo model/database.py
 
db = Database()

def create_item(table_name: str, item: dict):
    '''Adiciona um item a uma tabela específica no banco de dados'''
    db.conectar()
 
    try:
        if table_name == 'serie':
            sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES ( %s, %s, %s, %s)"
            params = (item['titulo'], item['descricao'], item['ano_lancamento'], item['id_categoria'])
        elif table_name == 'categoria':
            sql = "INSERT INTO categoria (categoria_nome) VALUES (%s)"
            params = (item['categoria_nome'],)
        elif table_name == 'ator':
            sql = "INSERT INTO ator (nome) VALUES (%s)"
            params = (item['nome'],)
        elif table_name == 'motivo_assistir':
            sql = "INSERT INTO motivo_assistir (id_serie, motivo) VALUES (%s, %s)"
            params = (item['id_serie'], item['motivo'])
        elif table_name == 'avaliacao_serie':
            sql = "INSERT INTO avaliacao_serie (id_serie, nota, comentario, data_avaliacao) VALUES (%s, %s, %s, NOW())"
            params = (item['id_serie'], item['nota'], item['comentario']) 

        else:
            raise HTTPException(status_code=400, detail="Tabela não permitida")
 
        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item adicionado com sucesso!"}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar o item: {str(e)}")