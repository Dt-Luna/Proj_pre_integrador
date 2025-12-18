from .dao import BaseDAO
from models.exemplar import Exemplar
from exceptions import ExemplarException, DAOException


class ExemplarDAO(BaseDAO):

    def inserir(self, exemplar):
        try:
            query = """
            INSERT INTO exemplar 
            (id_usuario, id_livro, status)
            VALUES (?, ?, ?)
            """
            params = (exemplar.id_usuario, exemplar.id_livro, exemplar.status)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir exemplar: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM exemplar"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar exemplares: {str(e)}")

    def listar_por_id(self, id_exemplar):
        try:
            query = "SELECT * FROM exemplar WHERE id_exemplar = ?"
            resultado = self._executar_query(query, (id_exemplar,), fetch_one=True)
            if not resultado:
                raise ExemplarException.ExemplarNaoEncontrado(f"Exemplar {id_exemplar} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplar: {str(e)}")

    def listar_por_usuario(self, id_usuario):
        try:
            query = "SELECT * FROM exemplar WHERE id_usuario = ?"
            return self._executar_query(query, (id_usuario,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplares do usuário: {str(e)}")

    def listar_por_livro(self, id_livro):
        try:
            query = "SELECT * FROM exemplar WHERE id_livro = ?"
            return self._executar_query(query, (id_livro,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplares do livro: {str(e)}")

    def listar_por_status(self, status):
        try:
            query = "SELECT * FROM exemplar WHERE status = ?"
            return self._executar_query(query, (status,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplares por status: {str(e)}")

    def atualizar(self, exemplar):
        try:
            query = """
            UPDATE exemplar 
            SET id_usuario = ?, id_livro = ?, status = ?
            WHERE id_exemplar = ?
            """
            params = (exemplar.id_usuario, exemplar.id_livro, 
                      exemplar.status, exemplar.id_exemplar)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar exemplar: {str(e)}")

    def excluir(self, id_exemplar):
        try:
            query = "DELETE FROM exemplar WHERE id_exemplar = ?"
            return self._executar_query(query, (id_exemplar,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir exemplar: {str(e)}")
