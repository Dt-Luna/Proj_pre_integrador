from exceptions import SistemaException, DAOException
from .dao import BaseDAO


class HistoricoEmprestimos:
    
    STATUS_ATIVO = "ativo"
    STATUS_CONCLUIDO = "concluído"
    STATUS_ATRASADO = "atrasado"
    STATUSES_VALIDOS = [STATUS_ATIVO, STATUS_CONCLUIDO, STATUS_ATRASADO]
    
    def __init__(self, id_historico, id_emprestimo, status_final):
        self._id_historico = id_historico
        self._id_emprestimo = id_emprestimo
        self._status_final = None
        self.set_status_final(status_final)

    def get_id(self):
        return self._id_historico
    
    def set_id(self, id_historico):
        self._id_historico = id_historico

    def get_id_emprestimo(self):
        return self._id_emprestimo
    
    def set_id_emprestimo(self, value):
        self._id_emprestimo = value

    def get_status_final(self):
        return self._status_final
    
    def set_status_final(self, value):
        if value not in self.STATUSES_VALIDOS:
            raise SistemaException(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status_final = value

    def __str__(self):
        return f"Histórico({self.get_id()}) - Empréstimo {self.get_id_emprestimo()}: {self.get_status_final()}"

    def __repr__(self):
        return f"HistoricoEmprestimos(id={self.get_id()})"

    def __eq__(self, other):
        if not isinstance(other, HistoricoEmprestimos):
            return False
        return self.get_id() == other.get_id()


class HistoricoEmprestimosDAO(BaseDAO):

    def inserir(self, historico):
        try:
            query = """
            INSERT INTO historico_emprestimos 
            (id_emprestimo, status_final)
            VALUES (?, ?)
            """
            params = (historico.get_id_emprestimo(), historico.get_status_final())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir histórico: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM historico_emprestimos"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar histórico: {str(e)}")

    def listar_id(self, id_historico):
        try:
            query = "SELECT * FROM historico_emprestimos WHERE id_historico = ?"
            resultado = self._executar_query(query, (id_historico,), fetch_one=True)
            if not resultado:
                raise DAOException.OperacaoFalhou(f"Histórico {id_historico} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar histórico: {str(e)}")

    def atualizar(self, historico):
        try:
            query = """
            UPDATE historico_emprestimos 
            SET id_emprestimo = ?, status_final = ?
            WHERE id_historico = ?
            """
            params = (historico.get_id_emprestimo(), historico.get_status_final(), 
                     historico.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar histórico: {str(e)}")

    def excluir(self, id_historico):
        try:
            query = "DELETE FROM historico_emprestimos WHERE id_historico = ?"
            return self._executar_query(query, (id_historico,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir histórico: {str(e)}")