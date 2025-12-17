"""
Classe Base DAO - Define a interface padrão para acesso a dados
Implementa o padrão de herança para todos os DAOs do sistema
"""
from abc import ABC, abstractmethod
from exceptions import DAOException
import logging

logger = logging.getLogger(__name__)


class BaseDAO(ABC):
    """
    Classe base abstrata para padrão DAO com banco de dados SQLite.
    Implementa herança e define contrato para subclasses.
    Todos os DAOs devem herdar desta classe.
    """

    def __init__(self, connection):
        """
        Inicializa o DAO com uma conexão ao banco de dados
        
        Args:
            connection: Conexão ativa com o banco SQLite
            
        Raises:
            DAOException.ConexaoFalhou: Se conexão inválida
        """
        if not connection:
            raise DAOException.ConexaoFalhou("Conexão ao banco de dados inválida")
        
        self.conn = connection
        self.cursor = self.conn.cursor()
        logger.debug(f"DAO {self.__class__.__name__} inicializado")

    @abstractmethod
    def inserir(self, obj):
        """Insere um objeto no banco de dados"""
        pass

    @abstractmethod
    def listar(self):
        """Lista todos os objetos"""
        pass

    @abstractmethod
    def listar_por_id(self, id):
        """Lista um objeto por ID"""
        pass

    @abstractmethod
    def atualizar(self, obj):
        """Atualiza um objeto no banco de dados"""
        pass

    @abstractmethod
    def excluir(self, id):
        """Exclui um objeto do banco de dados"""
        pass

    def _executar_query(self, query, params=None, fetch=False, fetch_one=False):
        """
        Executa uma query com tratamento de erro e logging
        
        Args:
            query: Comando SQL
            params: Parâmetros da query
            fetch: Se True, retorna fetchall()
            fetch_one: Se True, retorna fetchone()
            
        Returns:
            Resultado da query ou None em caso de erro
            
        Raises:
            DAOException.OperacaoFalhou: Se a operação falhar
        """
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
        """
        Converte uma linha de banco de dados em dicionário
        
        Args:
            colunas: Lista de nomes de colunas
            linha: Tupla com dados da linha
            
        Returns:
            Dicionário com dados
        """
        if not linha:
            return None
        return dict(zip(colunas, linha))

    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logger.info(f"Conexão do DAO {self.__class__.__name__} fechada")
