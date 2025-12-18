from .dao import BaseDAO
from models.avaliacaousuario import AvaliacaoUsuario
from exceptions import AvaliacaoException, DAOException


class AvaliacaoUsuarioDAO(BaseDAO):

    def inserir(self, avaliacao):
        try:
            query = """
            INSERT INTO avaliacao_usuario 
            (id_avaliador, id_avaliado, nota, comentario, data_avaliacao)
            VALUES (?, ?, ?, ?, ?)
            """
            params = (avaliacao.id_avaliador, avaliacao.id_avaliado, 
                      avaliacao.nota, avaliacao.comentario, avaliacao.data_avaliacao)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir avaliação: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM avaliacao_usuario"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar avaliações: {str(e)}")

    def listar_por_id(self, id_avaliacao):
        try:
            query = "SELECT * FROM avaliacao_usuario WHERE id_avaliacao = ?"
            resultado = self._executar_query(query, (id_avaliacao,), fetch_one=True)
            if not resultado:
                raise AvaliacaoException.AvaliacaoNaoEncontrada(f"Avaliação {id_avaliacao} não encontrada")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar avaliação: {str(e)}")

    def atualizar(self, avaliacao):
        try:
            query = """
            UPDATE avaliacao_usuario 
            SET id_avaliador = ?, id_avaliado = ?, nota = ?, 
                comentario = ?, data_avaliacao = ?
            WHERE id_avaliacao = ?
            """
            params = (avaliacao.id_avaliador, avaliacao.id_avaliado,
                      avaliacao.nota, avaliacao.comentario, 
                      avaliacao.data_avaliacao, avaliacao.id_avaliacao)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar avaliação: {str(e)}")

    def excluir(self, id_avaliacao):
        try:
            query = "DELETE FROM avaliacao_usuario WHERE id_avaliacao = ?"
            return self._executar_query(query, (id_avaliacao,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir avaliação: {str(e)}")