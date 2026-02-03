from exceptions import SolicitacaoException, DAOException
from .dao import BaseDAO
from datetime import datetime


class SolicitacaoEmprestimo:
    
    STATUS_PENDENTE = "pendente"
    STATUS_ACEITA = "aceita"
    STATUS_RECUSADA = "recusada"
    STATUS_CANCELADA = "cancelada"
    STATUSES_VALIDOS = [STATUS_PENDENTE, STATUS_ACEITA, STATUS_RECUSADA, STATUS_CANCELADA]
    
    def __init__(self, id_solicitacao, data, status=STATUS_PENDENTE, dias_emprestimo=None, id_exemplar=None, id_solicitante=None):
        self._id_solicitacao = id_solicitacao
        self._id_exemplar = id_exemplar
        self._dias_emprestimo = dias_emprestimo
        self._id_solicitante = id_solicitante
        self._data = None
        self._status = None
        
        self.set_data(data)
        self.set_status(status)

    def get_id(self):
        return self._id_solicitacao
    
    def set_id(self, id_solicitacao):
        self._id_solicitacao = id_solicitacao

    def set_dias_emprestimo(self, value):
        self._dias_emprestimo = value

    def get_dias_emprestimo(self):
        return self._dias_emprestimo

    def get_id_exemplar(self):
        return self._id_exemplar
    
    def set_id_exemplar(self, value):
        self._id_exemplar = value

    def get_id_solicitante(self):
        return self._id_solicitante
    
    def set_id_solicitante(self, value):
        self._id_solicitante = value

    def get_data(self):
        return self._data
    
    def set_data(self, value):
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise SolicitacaoException.DadosInvalidos(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )
        self._data = value

    def get_status(self):
        return self._status
    
    def set_status(self, value):
        if value not in self.STATUSES_VALIDOS:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status = value

    def aceitar(self):
        self.set_status(self.STATUS_ACEITA)

    def recusar(self):
        self.set_status(self.STATUS_RECUSADA)

    def cancelar(self):
        self.set_status(self.STATUS_CANCELADA)

    def esta_pendente(self):
        return self.get_status() == self.STATUS_PENDENTE

    def __str__(self):
        return f"Solicitação({self.get_id()}) - Status: {self.get_status()}"

    def __repr__(self):
        return f"SolicitacaoEmprestimo(id={self.get_id()}, exemplar={self.get_id_exemplar()})"

    def __eq__(self, other):
        if not isinstance(other, SolicitacaoEmprestimo):
            return False
        return self.get_id() == other.get_id()

    def to_df(self):
        return {
            'ID': self.get_id(),
            'Data': self.get_data(),
            'Status': self.get_status(),
            'Dias': self.get_dias_emprestimo(),
            'Exemplar': self.get_id_exemplar(),
            'Solicitante': self.get_id_solicitante()
        }


class SolicitacaoEmprestimoDAO(BaseDAO):

    def inserir(self, solicitacao):
        try:
            query = """
            INSERT INTO solicitacao_emprestimo
            (data_solicitacao, status, dias_emprestimo, id_exemplar, id_solicitante)
            VALUES (?, ?, ?, ?, ?)
            """
            params = (solicitacao.get_data(), solicitacao.get_status(), solicitacao.get_dias_emprestimo(),
                     solicitacao.get_id_exemplar(), solicitacao.get_id_solicitante())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir solicitação: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM solicitacao_emprestimo"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar solicitações: {str(e)}")

    def listar_id(self, id_solicitacao):
        try:
            query = "SELECT * FROM solicitacao_emprestimo WHERE id_solicitacao = ?"
            resultado = self._executar_query(query, (id_solicitacao,), fetch_one=True)
            if not resultado:
                raise SolicitacaoException.SolicitacaoNaoEncontrada(f"Solicitação {id_solicitacao} não encontrada")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar solicitação: {str(e)}")

    def atualizar(self, solicitacao):
        try:
            query = """
            UPDATE solicitacao_emprestimo
            SET data_solicitacao = ?, status = ?, dias_emprestimo = ?, id_exemplar = ?, id_solicitante = ?
            WHERE id_solicitacao = ?
            """
            params = (solicitacao.get_data(), solicitacao.get_status(), solicitacao.get_dias_emprestimo(),
                     solicitacao.get_id_exemplar(), solicitacao.get_id_solicitante(), solicitacao.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar solicitação: {str(e)}")

    def excluir(self, id_solicitacao):
        try:
            query = "DELETE FROM solicitacao_emprestimo WHERE id_solicitacao = ?"
            return self._executar_query(query, (id_solicitacao,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir solicitação: {str(e)}")

    def listar_por_usuario(self, id_usuario):
        try:
            query = "SELECT * FROM solicitacao_emprestimo WHERE id_solicitante = ?"
            return self._executar_query(query, (id_usuario,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar solicitações por usuário: {str(e)}")

    def listar_por_exemplar(self, id_exemplar):
        try:
            query = "SELECT * FROM solicitacao_emprestimo WHERE id_exemplar = ?"
            return self._executar_query(query, (id_exemplar,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar solicitações por exemplar: {str(e)}")

    def listar_pendentes_por_dono(self, id_dono):
        try:
            query = """
            SELECT s.* FROM solicitacao_emprestimo s
            JOIN exemplar e ON s.id_exemplar = e.id_exemplar
            WHERE e.id_usuario = ? AND s.status = 'pendente'
            """
            return self._executar_query(query, (id_dono,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar solicitações pendentes por dono: {str(e)}")
