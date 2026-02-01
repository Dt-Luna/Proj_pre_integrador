from abc import ABC, abstractmethod
import logging
import sqlite3

logger = logging.getLogger(__name__)

class BaseDAO(ABC):

    def __init__(self, connection):
        from exceptions import DAOException
        
        if not connection:
            raise DAOException.ConexaoFalhou("Conexão ao banco de dados inválida")
        
        self.conn = connection
        self.cursor = self.conn.cursor()
        logger.debug(f"DAO {self.__class__.__name__} inicializado")

    @abstractmethod
    def inserir(self, obj):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def listar_id(self, id):
        pass

    @abstractmethod
    def atualizar(self, obj):
        pass

    @abstractmethod
    def excluir(self, id):
        pass

    def _executar_query(self, query, params=None, fetch=False, fetch_one=False):
        from exceptions import DAOException
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if not query.strip().upper().startswith("SELECT"):
                self.conn.commit()
                logger.debug(f"Query executada com sucesso: {query[:50]}...")
            
            if fetch:
                return self.cursor.fetchall()
            elif fetch_one:
                return self.cursor.fetchone()
            else:
                return self.cursor.lastrowid
                
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Erro ao executar query: {e}")
            raise DAOException.OperacaoFalhou(f"Erro ao executar operação: {str(e)}")

    def _converter_str_to_data(data_str):
        from datetime import datetime
        if data_str:
            return datetime.strptime(data_str, "%Y-%m-%d").date()
        return None

    def _converter_data_to_str(data):
        if data:
            return data.strftime("%Y-%m-%d")
        return None

    def _converter_linha_para_objeto(self, colunas, linha, classe):
        if not linha:
            return None
            
        return dict(zip(colunas, linha))
    
    @staticmethod
    def criar_admin_padrao():
        conn = sqlite3.connect('bookshare.db')
        cursor = conn.cursor()
        
        # Supondo que 'email' seja UNIQUE no seu banco
        sql = """
        INSERT OR IGNORE INTO usuario (username, senha, data_nascimento, email) 
        VALUES ('Administrador', '123456', '2000-01-01', 'admin@sistema.com')
        """
        
        cursor.execute(sql)
        conn.commit()
        conn.close()


    def fechar(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logger.info(f"Conexão do DAO {self.__class__.__name__} fechada")