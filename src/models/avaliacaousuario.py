from exceptions import AvaliacaoException, DAOException
from .dao import BaseDAO
from datetime import datetime


class AvaliacaoUsuario:
    NOTA_MINIMA = 1
    NOTA_MAXIMA = 5
    
    def __init__(self, id_avaliacao, id_avaliador, tipo_avaliador, nota, comentario, data_avaliacao):
        self._id_avaliacao = id_avaliacao
        self._id_avaliador = id_avaliador
        self._tipo_avaliador = tipo_avaliador
        self._nota = None
        self._comentario = None
        self._data_avaliacao = None
        
        self.set_nota(nota)
        self.set_comentario(comentario)
        self.set_data_avaliacao(data_avaliacao)

    def get_id(self):
        return self._id_avaliacao
    
    def set_id(self, id_avaliacao):
        self._id_avaliacao = id_avaliacao

    def get_id_avaliador(self):
        return self._id_avaliador
    
    def set_id_avaliador(self, value):
        self._id_avaliador = value

    def get_tipo_avaliador(self):
        return self._tipo_avaliador
    
    def set_tipo_avaliador(self, value):
        self._tipo_avaliador = value

    def get_nota(self):
        return self._nota
    
    def set_nota(self, value):
        valor_int = int(value)
        if valor_int < self.NOTA_MINIMA or valor_int > self.NOTA_MAXIMA:
            raise AvaliacaoException.AvaliacaoInvalida(
                f"Nota deve estar entre {self.NOTA_MINIMA} e {self.NOTA_MAXIMA}"
            )
        self._nota = valor_int

    def get_comentario(self):
        return self._comentario
    
    def set_comentario(self, value):
        if value and len(value.strip()) > 500:
            raise AvaliacaoException.AvaliacaoInvalida(
                "Comentário não pode exceder 500 caracteres"
            )
        self._comentario = value.strip() if value else ""

    def get_data_avaliacao(self):
        return self._data_avaliacao
    
    def set_data_avaliacao(self, value):
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise AvaliacaoException.AvaliacaoInvalida(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )
        self._data_avaliacao = value

    def __str__(self):
        return f"Avaliação: {self.get_nota()}/5 - '{self.get_comentario()[:30]}...'"

    def __repr__(self):
        return f"AvaliacaoUsuario(id={self.get_id()}, nota={self.get_nota()})"

    def __eq__(self, other):
        if not isinstance(other, AvaliacaoUsuario):
            return False
        return self.get_id() == other.get_id()


class AvaliacaoUsuarioDAO(BaseDAO):

    def inserir(self, avaliacao):
        try:
            query = """
            INSERT INTO avaliacao_usuario 
            (id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (avaliacao.get_id_avaliador(), avaliacao.get_tipo_avaliador(), 
                     avaliacao.get_nota(), avaliacao.get_comentario(), 
                     avaliacao.get_id_emprestimo(), avaliacao.get_data_avaliacao())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir avaliação: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM avaliacao_usuario"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar avaliações: {str(e)}")

    def listar_por_avaliador_emprestimo(self, id_avaliador, id_emprestimo):
        try:
            query = "SELECT * FROM avaliacao_usuario WHERE id_avaliador = ? AND id_emprestimo = ?"
            resultado = self._executar_query(query, (id_avaliador, id_emprestimo), fetch_one=True)
            if not resultado:
                raise AvaliacaoException.AvaliacaoNaoEncontrada(
                    f"Avaliação não encontrada para avaliador {id_avaliador} e empréstimo {id_emprestimo}"
                )
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar avaliação: {str(e)}")

# avaliacao vai ser salvo com chave composta de id_avaliador e id_emprestimo, mas na duvida deixa o codigo de id_avaliacao comentado
    def listar_id(self, id_avaliacao):
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
            SET id_avaliador = ?, tipo_avaliador = ?, nota = ?, 
                comentario = ?, data_avaliacao = ?
            WHERE id_avaliacao = ?
            """
            params = (avaliacao.get_id_avaliador(), avaliacao.get_tipo_avaliador(),
                     avaliacao.get_nota(), avaliacao.get_comentario(), 
                     avaliacao.get_data_avaliacao(), avaliacao.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar avaliação: {str(e)}")

    def excluir(self, id_avaliacao):
        try:
            query = "DELETE FROM avaliacao_usuario WHERE id_avaliacao = ?"
            return self._executar_query(query, (id_avaliacao,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir avaliação: {str(e)}")