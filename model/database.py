import mysql.connector as mc
from mysql.connector import Error, MySQLConnection
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Any, Tuple, List, Union

class Database:
    def __init__(self) -> None:  
        load_dotenv()
        self.host = getenv('DB_HOST')
        self.username:  str = getenv('DB_USER')
        self.password: str = getenv('DB_PSWD')
        self.database : str =getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None
        self.cursor: Optional[Union[List[dict], None]] = None # Incialização do cursor 

    def conectar(self) -> None:
        """Estabele uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password = self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print('Conexão com o bdc realizada com sucesso!')
 
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursot = None
 
    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se
        existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print('Conexão com o bcd encerrada')
 
    def executar(self, sql: str, params:Optional[Tuple[Any, ...]] = None) -> Optional[List[dict]]:
        """Executa uma instrução no banco de dados."""
        if self.connection is None or self.cursor is None:
            print('Conexão não estabelecida!')
            return None
       
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor
        except Error as e:
            print(f'Erro de execução: {e}')
            return None
       
 
    def consultar(self, sql: str, params: Optional[Tuple[Any, ...]]=None) -> Optional[List[dict]]:
        """Executa uma consulta no banco de dados."""
        if self.connection is None and self.cursor is None:
            print('Conexão com o bcd não estabelecida!')
            return None
       
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f'Erro de consulta: {e}')
            return None
    
db = Database()
db.conectar()
db.desconectar()