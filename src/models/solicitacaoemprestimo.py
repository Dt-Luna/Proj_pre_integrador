class SolicitacaoEmprestimo:
    """Modelo de solicitação de empréstimo"""
    
    def __init__(self, id_solicitacao, id_exemplar, id_solicitante, data, status):
        self.id_solicitacao = id_solicitacao
        self.id_exemplar = id_exemplar
        self.id_solicitante = id_solicitante
        self.data = data
        self.status = status

    def __str__(self):
        return f"Solicitação({self.id_exemplar}) - {self.status} - {self.data}"

    def __repr__(self):
        return f"SolicitacaoEmprestimo(id={self.id_solicitacao}, status='{self.status}')"