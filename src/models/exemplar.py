class Exemplar:
    """Modelo de exemplar de livro"""
    
    def __init__(self, id_exemplar, id_usuario, id_livro, status):
        self.id_exemplar = id_exemplar
        self.id_usuario = id_usuario
        self.id_livro = id_livro
        self.status = status

    def __str__(self):
        return f"Exemplar({self.id_exemplar}) - Livro:{self.id_livro} - Status:{self.status}"

    def __repr__(self):
        return f"Exemplar(id={self.id_exemplar}, livro={self.id_livro}, status='{self.status}')"