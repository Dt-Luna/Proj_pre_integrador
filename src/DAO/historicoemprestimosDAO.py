from .dao import BaseDAO
from models.historicoemprestimos import HistoricoEmprestimos
from exceptions import DAOException


class HistoricoEmprestimosDAO(BaseDAO):
    """DAO para gerenciar histórico de empréstimos - Herda de BaseDAO"""

    def inserir(self, historico):
        """Insere um novo registro de histórico"""
        try:
            query = """
            INSERT INTO historico_emprestimos 
            (id_emprestimo, status_final)
            VALUES (?, ?)
            """
            params = (historico.id_emprestimo, historico.status_final)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir histórico: {str(e)}")

    def listar(self):
        """Lista todo o histórico"""
        try:
            query = "SELECT * FROM historico_emprestimos"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar histórico: {str(e)}")

    def listar_por_id(self, id_historico):
        """Lista um registro de histórico por ID"""
        try:
            query = "SELECT * FROM historico_emprestimos WHERE id_historico = ?"
            resultado = self._executar_query(query, (id_historico,), fetch_one=True)
            if not resultado:
                raise DAOException.OperacaoFalhou(f"Histórico {id_historico} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar histórico: {str(e)}")

    def atualizar(self, historico):
        """Atualiza um registro de histórico"""
        try:
            query = """
            UPDATE historico_emprestimos 
            SET id_emprestimo = ?, status_final = ?
            WHERE id_historico = ?
            """
            params = (historico.id_emprestimo, historico.status_final, historico.id_historico)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar histórico: {str(e)}")

    def excluir(self, id_historico):
        """Exclui um registro de histórico"""
        try:
            query = "DELETE FROM historico_emprestimos WHERE id_historico = ?"
            return self._executar_query(query, (id_historico,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir histórico: {str(e)}")