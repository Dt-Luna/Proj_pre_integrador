from abc import ABC, abstractmethod
from exceptions import DAOException
import logging

logger = logging.getLogger(__name__)


class BaseDAO(ABC):

    def __init__(self, connection):
        """
            DAOException.ConexaoFalhou: Se conexão inválida
        """
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
    def listar_por_id(self, id):
        pass

    @abstractmethod
    def atualizar(self, obj):
        pass

    @abstractmethod
    def excluir(self, id):
        pass

    def _executar_query(self, query, params=None, fetch=False, fetch_one=False):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # Commit apenas se não for SELECT
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

    def _converter_linha_para_dicionario(self, colunas, linha):
        if not linha:
            return None
        return dict(zip(colunas, linha))

    def fechar(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logger.info(f"Conexão do DAO {self.__class__.__name__} fechada")
