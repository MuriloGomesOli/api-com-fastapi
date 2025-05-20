from fastapi import HTTPException
from model.database import Database, TABELAS
from model.database import Ator_serie


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
                marcador += ', NOW()'

            sql = f"INSERT INTO {table_name} ({colunas}) VALUES ({marcador})"
            params = tuple(item[colunas] for colunas in columns)

            db.executar(sql, params)
            db.desconectar()

            return {"message": "Item adicionado com sucesso!"}

        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao adicionar o item: {str(e)}")
    



def criar_ator_serie(ator : Ator_serie):

    db = Database()
    db.conectar()

    query = f"Select id_autor from ator where (nome like '%{ator.nome_ator}%') limit 1"
    id_ator = db.select(query) #retorna uma lista de tuplas
    id_ator = id_ator[0]['id_autor']

    query = f"Select id_serie from serie where (titulo like '%{ator.titulo}%') limit 1"
    id_serie = db.select(query) #retorna uma lista de tuplas
    id_serie = id_serie[0]['id_serie']



    sql = "INSERT INTO ator_serie (id_serie, id_ator, personagem) VALUES (%s, %s,%s)"
    db.executar(sql,(id_serie,id_ator, ator.personagem))
    db.desconectar()
    return {"mensagem": "Série vinculada ao ator com sucesso"}