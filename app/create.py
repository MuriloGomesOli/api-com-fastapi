from fastapi import HTTPException
from model.database import Database, table
from model.database import Ator_serie


db = Database()
tb = table()

def get_nome_coluna(table_name: str):
    return {
        "serie": "titulo",
        "categoria": "nome_categoria",
        "ator": "nome",
        "ator_serie": "personagem"
    }.get(table_name)


def get_id_by_name(table_name: str, nome: str):
    
    coluna = get_nome_coluna(table_name)
    if not coluna:
        raise HTTPException(status_code=400, detail="Tabela não permitida")
    
    with Database() as db:

        query = f"SELECT {tb.PRIMARY_KEYS[table_name]} FROM {table_name} WHERE {coluna} LIKE %s LIMIT 1"
        resultado = db.consultar(query, (f"%{nome}%",))

        if not resultado:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        return resultado[0][tb.PRIMARY_KEYS[table_name]]


@staticmethod
def create_item(table_name: str, item: dict):
        if table_name not in tb.TABELAS:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        columns = tb.TABELAS[table_name]
        colunas = ', '.join(columns)
        marcador = ', '.join(['%s'] * len(columns))

        # Caso especial para avaliacao_serie com NOW()
        if table_name == 'avaliacao_serie':
            colunas += ', data_avaliacao'
            marcador += ', NOW()'

        sql = f"INSERT INTO {table_name} ({colunas}) VALUES ({marcador})"
        params = tuple(item[col] for col in columns)

        try:
            with Database() as db:
                db.executar(sql, params)
            return {"message": "Item adicionado com sucesso!"}
        except Exception as e:
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