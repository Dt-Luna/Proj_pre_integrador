from abc import ABC, abstractmethod


class BaseDAO(ABC):
    """Classe base abstrata para padrão DAO com banco de dados SQLite"""

    def __init__(self, connection):
        """
        Inicializa o DAO com uma conexão ao banco de dados
        
        Args:
            connection: Conexão ativa com o banco SQLite
        """
        self.conn = connection
        self.cursor = self.conn.cursor()

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

    def _executar_query(self, query, params=None):
        """
        Executa uma query com tratamento de erro
        
        Args:
            query: Comando SQL
            params: Parâmetros da query
            
        Returns:
            Resultado da query ou None em caso de erro
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao executar query: {e}")
            return None