from fastapi import HTTPException
from model.database import Database # importa a classe Database do arquivo model/database.py
 
db = Database()

def update_item(table_name: str, item_id: int, item: dict):
    '''Atualiza um item de uma tabela específica no banco de dados'''
    db.conectar()
 
    try:
        if table_name == 'serie':
            sql = """
                UPDATE serie
                SET titulo = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s
                WHERE id_serie = %s
            """
            params = (item['titulo'], item['descricao'], item['ano_lancamento'], item['id_categoria'], item_id)
        elif table_name == 'categoria':
            sql = "UPDATE categoria SET categoria_nome = %s WHERE id_categoria = %s"
            params = (item['categoria_nome'], item_id)
        elif table_name == 'ator':
            sql = "UPDATE ator SET nome = %s WHERE id_ator = %s"
            params = (item['nome'], item_id)
        elif table_name == 'motivo_assistir':
            sql = "UPDATE motivo_assistir SET id_serie = %s, motivo = %s WHERE id_motivo = %s"
            params = (item['id_serie'], item['motivo'], item_id)
        elif table_name == 'avaliacao_serie':
            sql = """
                UPDATE avaliacao_serie
                SET id_serie = %s, nota = %s, comentario = %s
                WHERE id_avaliacao = %s
            """
            params = (item['id_serie'], item['nota'], item['comentario'], item_id)

        else:
            raise HTTPException(status_code=400, detail="Tabela não permitida")
 
        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item atualizado com sucesso!"}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item: {str(e)}")