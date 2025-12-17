"""
Modelo de Solicitação de Empréstimo - Implementa encapsulamento com propriedades
"""
from exceptions import SolicitacaoException
from datetime import datetime


class SolicitacaoEmprestimo:
    """
    Modelo de solicitação de empréstimo do sistema.
    Implementa encapsulamento de atributos com validação.
    """
    
    STATUS_PENDENTE = "pendente"
    STATUS_ACEITA = "aceita"
    STATUS_RECUSADA = "recusada"
    STATUS_CANCELADA = "cancelada"
    STATUSES_VALIDOS = [STATUS_PENDENTE, STATUS_ACEITA, STATUS_RECUSADA, STATUS_CANCELADA]
    
    def __init__(self, id_solicitacao, id_exemplar, id_solicitante, data, status=STATUS_PENDENTE):
        """
        Inicializa uma nova solicitação de empréstimo
        
        Args:
            id_solicitacao: ID único da solicitação
            id_exemplar: ID do exemplar solicitado
            id_solicitante: ID do usuário que solicita
            data: Data da solicitação
            status: Status da solicitação
            
        Raises:
            SolicitacaoException.DadosInvalidos: Se dados inválidos
        """
        self._id_solicitacao = id_solicitacao
        self._id_exemplar = id_exemplar
        self._id_solicitante = id_solicitante
        self.data = data  # Usa property
        self.status = status  # Usa property

    @property
    def id_solicitacao(self):
        """Getter do ID da solicitação"""
        return self._id_solicitacao

    @property
    def id_exemplar(self):
        """Getter do ID do exemplar"""
        return self._id_exemplar

    @property
    def id_solicitante(self):
        """Getter do ID do solicitante"""
        return self._id_solicitante

    @property
    def data(self):
        """Getter da data"""
        return self._data
    
    @data.setter
    def data(self, value):
        """Setter com validação da data"""
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise SolicitacaoException.DadosInvalidos(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )
        self._data = value

    @property
    def status(self):
        """Getter do status"""
        return self._status
    
    @status.setter
    def status(self, value):
        """Setter com validação do status"""
        if value not in self.STATUSES_VALIDOS:
            raise SolicitacaoException.DadosInvalidos(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status = value

    def aceitar(self):
        """Aceita a solicitação"""
        if self.status != self.STATUS_PENDENTE:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Não é possível aceitar solicitação com status: {self.status}"
            )
        self.status = self.STATUS_ACEITA

    def recusar(self):
        """Recusa a solicitação"""
        if self.status != self.STATUS_PENDENTE:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Não é possível recusar solicitação com status: {self.status}"
            )
        self.status = self.STATUS_RECUSADA

    def cancelar(self):
        """Cancela a solicitação"""
        if self.status not in [self.STATUS_PENDENTE, self.STATUS_ACEITA]:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Não é possível cancelar solicitação com status: {self.status}"
            )
        self.status = self.STATUS_CANCELADA

    def esta_pendente(self):
        """Verifica se a solicitação está pendente"""
        return self.status == self.STATUS_PENDENTE

    def __str__(self):
        """Representação em string da solicitação"""
        return f"Solicitação({self.id_exemplar}) - {self.status} - {self.data}"

    def __repr__(self):
        """Representação técnica da solicitação"""
        return f"SolicitacaoEmprestimo(id={self.id_solicitacao}, status='{self.status}')"

    def __eq__(self, other):
        """Compara solicitações por ID"""
        if not isinstance(other, SolicitacaoEmprestimo):
            return False
        return self.id_solicitacao == other.id_solicitacao
