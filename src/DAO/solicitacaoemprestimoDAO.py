from .dao import BaseDAO
from models.solicitacaoemprestimo import SolicitacaoEmprestimo
from exceptions import SolicitacaoException, DAOException


class SolicitacaoEmprestimoDAO(BaseDAO):
    """DAO para gerenciar solicitações de empréstimo - Herda de BaseDAO"""

    def inserir(self, solicitacao):
        """Insere uma nova solicitação de empréstimo"""
        try:
            query = """
            INSERT INTO solicitacao_emprestimo 
            (id_exemplar, id_solicitante, data_solicitacao, status)
            VALUES (?, ?, ?, ?)
            """
            params = (solicitacao.id_exemplar, solicitacao.id_solicitante, 
                      solicitacao.data, solicitacao.status)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir solicitação: {str(e)}")

    def listar(self):
        """Lista todas as solicitações"""
        try:
            query = "SELECT * FROM solicitacao_emprestimo"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar solicitações: {str(e)}")

    def listar_por_id(self, id_solicitacao):
        """Lista uma solicitação por ID"""
        try:
            query = "SELECT * FROM solicitacao_emprestimo WHERE id_solicitacao = ?"
            resultado = self._executar_query(query, (id_solicitacao,), fetch_one=True)
            if not resultado:
                raise SolicitacaoException.SolicitacaoNaoEncontrada(f"Solicitação {id_solicitacao} não encontrada")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar solicitação: {str(e)}")

    def atualizar(self, solicitacao):
        """Atualiza uma solicitação existente"""
        try:
            query = """
            UPDATE solicitacao_emprestimo 
            SET id_exemplar = ?, id_solicitante = ?, data_solicitacao = ?, status = ?
            WHERE id_solicitacao = ?
            """
            params = (solicitacao.id_exemplar, solicitacao.id_solicitante,
                      solicitacao.data, solicitacao.status, solicitacao.id_solicitacao)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar solicitação: {str(e)}")

    def excluir(self, id_solicitacao):
        """Exclui uma solicitação"""
        try:
            query = "DELETE FROM solicitacao_emprestimo WHERE id_solicitacao = ?"
            return self._executar_query(query, (id_solicitacao,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir solicitação: {str(e)}")