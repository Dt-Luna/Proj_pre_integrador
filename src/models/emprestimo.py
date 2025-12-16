class Emprestimo:
    """Modelo de empréstimo de livro"""
    
    def __init__(self, id_emprestimo, id_exemplar, id_dono, id_emprestado,
                 data_inicio, data_prevista, data_devolucao=None):
        self.id_emprestimo = id_emprestimo
        self.id_exemplar = id_exemplar
        self.id_dono = id_dono
        self.id_emprestado = id_emprestado
        self.data_inicio = data_inicio
        self.data_prevista = data_prevista
        self.data_devolucao = data_devolucao

    def __str__(self):
        status = "Devolvido" if self.data_devolucao else "Ativo"
        return f"Empréstimo({self.id_exemplar}) - {status} - Prazo: {self.data_prevista}"

    def __repr__(self):
        return f"Emprestimo(id={self.id_emprestimo}, exemplar={self.id_exemplar})"