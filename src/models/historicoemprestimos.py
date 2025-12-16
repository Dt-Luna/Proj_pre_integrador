class HistoricoEmprestimos:
    """Modelo de histórico de empréstimos"""
    
    def __init__(self, id_historico, id_emprestimo, status_final):
        self.id_historico = id_historico
        self.id_emprestimo = id_emprestimo
        self.status_final = status_final

    def __str__(self):
        return f"Histórico(Empréstimo:{self.id_emprestimo}, Status:{self.status_final})"

    def __repr__(self):
        return f"HistoricoEmprestimos(id={self.id_historico}, status='{self.status_final}')"