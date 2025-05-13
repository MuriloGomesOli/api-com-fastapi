from fastapi import HTTPException
from model.database import Database # importa a classe Database do arquivo model/database.py
 
db = Database()

def delete_item(table_name: str, item_id: int):
    '''Remove um item de uma tabela específica no banco de dados'''
    db.conectar()
    
    try:
        if table_name == 'serie':
            sql = "DELETE FROM serie WHERE id_serie = %s"
        elif table_name == 'categoria':
            sql = "DELETE FROM categoria WHERE id_categoria = %s"
        elif table_name == 'ator':
            sql = "DELETE FROM ator WHERE id_ator = %s"
        elif table_name == 'motivo_assistir':
            sql = "DELETE FROM motivo_assistir WHERE id_motivo = %s"
        elif table_name == 'avaliacao_serie':
            sql = "DELETE FROM avaliacao_serie WHERE id_avaliacao = %s"
        else:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        db.executar(sql, (item_id,))
        db.desconectar()

        return {"message": "Item removido com sucesso!"}
    
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao remover o item: {str(e)}")