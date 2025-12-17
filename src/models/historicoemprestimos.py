"""
Modelo de Histórico de Empréstimos - Implementa encapsulamento com propriedades
"""
from exceptions import SistemaException


class HistoricoEmprestimos:
    """
    Modelo de histórico de empréstimos do sistema.
    Implementa encapsulamento de atributos com validação.
    """
    
    STATUS_ATIVO = "ativo"
    STATUS_CONCLUIDO = "concluído"
    STATUS_ATRASADO = "atrasado"
    STATUSES_VALIDOS = [STATUS_ATIVO, STATUS_CONCLUIDO, STATUS_ATRASADO]
    
    def __init__(self, id_historico, id_emprestimo, status_final):
        """
        Inicializa um novo registro de histórico
        
        Args:
            id_historico: ID único do histórico
            id_emprestimo: ID do empréstimo
            status_final: Status final do empréstimo
            
        Raises:
            SistemaException: Se dados inválidos
        """
        self._id_historico = id_historico
        self._id_emprestimo = id_emprestimo
        self.status_final = status_final  # Usa property

    @property
    def id_historico(self):
        """Getter do ID do histórico"""
        return self._id_historico

    @property
    def id_emprestimo(self):
        """Getter do ID do empréstimo"""
        return self._id_emprestimo

    @property
    def status_final(self):
        """Getter do status final"""
        return self._status_final
    
    @status_final.setter
    def status_final(self, value):
        """Setter com validação do status final"""
        if value not in self.STATUSES_VALIDOS:
            raise SistemaException(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status_final = value

    def __str__(self):
        """Representação em string do histórico"""
        return f"Histórico(Empréstimo:{self.id_emprestimo}, Status:{self.status_final})"

    def __repr__(self):
        """Representação técnica do histórico"""
        return f"HistoricoEmprestimos(id={self.id_historico}, status='{self.status_final}')"

    def __eq__(self, other):
        """Compara históricos por ID"""
        if not isinstance(other, HistoricoEmprestimos):
            return False
        return self.id_historico == other.id_historico
