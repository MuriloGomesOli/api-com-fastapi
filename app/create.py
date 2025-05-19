from fastapi import HTTPException
from model.database import Database, TABELAS

db = Database()


def create_item(table_name: str, item: dict):
    '''Adiciona um item a uma tabela específica no banco de dados'''
    db.conectar()

    try:
        if table_name not in TABELAS:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        columns = TABELAS[table_name]
        colunas = ', '.join(columns)
        marcador = ', '.join(['%s'] * len(columns))

        # Caso especial para avaliacao_serie com NOW()
        if table_name == 'avaliacao_serie':
            colunas += ', data_avaliacao'
            placeholders += ', NOW()'

        sql = f"INSERT INTO {table_name} ({colunas}) VALUES ({marcador})"
        params = tuple(item[colunas] for colunas in columns)

        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item adicionado com sucesso!"}

    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar o item: {str(e)}")
