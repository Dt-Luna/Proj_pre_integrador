from .dao import BaseDAO
from models.emprestimo import Emprestimo
from exceptions import EmprestimoException, DAOException


class EmprestimoDAO(BaseDAO):

    def inserir(self, emprestimo):
        try:
            query = """
            INSERT INTO emprestimo 
            (id_exemplar, id_dono, id_emprestado, data_inicio, data_prevista, data_devolucao)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (emprestimo.id_exemplar, emprestimo.id_dono, emprestimo.id_emprestado,
                      emprestimo.data_inicio, emprestimo.data_prevista, emprestimo.data_devolucao)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir empréstimo: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM emprestimo"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar empréstimos: {str(e)}")

    def listar_por_id(self, id_emprestimo):
        try:
            query = "SELECT * FROM emprestimo WHERE id_emprestimo = ?"
            resultado = self._executar_query(query, (id_emprestimo,), fetch_one=True)
            if not resultado:
                raise EmprestimoException.EmprestimoNaoEncontrado(f"Empréstimo {id_emprestimo} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar empréstimo: {str(e)}")

    def atualizar(self, emprestimo):
        try:
            query = """
            UPDATE emprestimo 
            SET id_exemplar = ?, id_dono = ?, id_emprestado = ?, 
                data_inicio = ?, data_prevista = ?, data_devolucao = ?
            WHERE id_emprestimo = ?
            """
            params = (emprestimo.id_exemplar, emprestimo.id_dono, emprestimo.id_emprestado,
                      emprestimo.data_inicio, emprestimo.data_prevista, 
                      emprestimo.data_devolucao, emprestimo.id_emprestimo)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar empréstimo: {str(e)}")

    def excluir(self, id_emprestimo):
        try:
            query = "DELETE FROM emprestimo WHERE id_emprestimo = ?"
            return self._executar_query(query, (id_emprestimo,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir empréstimo: {str(e)}")