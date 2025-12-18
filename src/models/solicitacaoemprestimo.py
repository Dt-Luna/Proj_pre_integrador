from exceptions import SolicitacaoException
from datetime import datetime


class SolicitacaoEmprestimo:
    
    STATUS_PENDENTE = "pendente"
    STATUS_ACEITA = "aceita"
    STATUS_RECUSADA = "recusada"
    STATUS_CANCELADA = "cancelada"
    STATUSES_VALIDOS = [STATUS_PENDENTE, STATUS_ACEITA, STATUS_RECUSADA, STATUS_CANCELADA]
    
    def __init__(self, id_solicitacao, id_exemplar, id_solicitante, data, status=STATUS_PENDENTE):
        self._id_solicitacao = id_solicitacao
        self._id_exemplar = id_exemplar
        self._id_solicitante = id_solicitante
        self.data = data  
        self.status = status  

    @property
    def id_solicitacao(self):
        return self._id_solicitacao

    @property
    def id_exemplar(self):
        return self._id_exemplar

    @property
    def id_solicitante(self):
        return self._id_solicitante

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
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
        return self._status
    
    @status.setter
    def status(self, value):
        if value not in self.STATUSES_VALIDOS:
            raise SolicitacaoException.DadosInvalidos(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status = value

    def aceitar(self):
        if self.status != self.STATUS_PENDENTE:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Não é possível aceitar solicitação com status: {self.status}"
            )
        self.status = self.STATUS_ACEITA

    def recusar(self):
        if self.status != self.STATUS_PENDENTE:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Não é possível recusar solicitação com status: {self.status}"
            )
        self.status = self.STATUS_RECUSADA

    def cancelar(self):
        if self.status not in [self.STATUS_PENDENTE, self.STATUS_ACEITA]:
            raise SolicitacaoException.SolicitacaoInvalida(
                f"Não é possível cancelar solicitação com status: {self.status}"
            )
        self.status = self.STATUS_CANCELADA

    def esta_pendente(self):
        return self.status == self.STATUS_PENDENTE

    def __str__(self):
        return f"Solicitação({self.id_exemplar}) - {self.status} - {self.data}"

    def __repr__(self):
        """Representação técnica da solicitação"""
        return f"SolicitacaoEmprestimo(id={self.id_solicitacao}, status='{self.status}')"

    def __eq__(self, other):
        """Compara solicitações por ID"""
        if not isinstance(other, SolicitacaoEmprestimo):
            return False
        return self.id_solicitacao == other.id_solicitacao
