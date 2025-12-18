from exceptions import SistemaException


class HistoricoEmprestimos:
    
    STATUS_ATIVO = "ativo"
    STATUS_CONCLUIDO = "concluído"
    STATUS_ATRASADO = "atrasado"
    STATUSES_VALIDOS = [STATUS_ATIVO, STATUS_CONCLUIDO, STATUS_ATRASADO]
    
    def __init__(self, id_historico, id_emprestimo, status_final):
        self._id_historico = id_historico
        self._id_emprestimo = id_emprestimo
        self.status_final = status_final 

    @property
    def id_historico(self):
        return self._id_historico

    @property
    def id_emprestimo(self):
        return self._id_emprestimo

    @property
    def status_final(self):
        return self._status_final
    
    @status_final.setter
    def status_final(self, value):
        if value not in self.STATUSES_VALIDOS:
            raise SistemaException(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status_final = value

    def __str__(self):
        return f"Histórico(Empréstimo:{self.id_emprestimo}, Status:{self.status_final})"

    def __repr__(self):
        """Representação técnica do histórico"""
        return f"HistoricoEmprestimos(id={self.id_historico}, status='{self.status_final}')"

    def __eq__(self, other):
        """Compara históricos por ID"""
        if not isinstance(other, HistoricoEmprestimos):
            return False
        return self.id_historico == other.id_historico
