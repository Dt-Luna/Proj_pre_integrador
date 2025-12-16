class Livro:
    """Modelo de livro do sistema"""
    
    def __init__(self, id_livro, titulo, autor, paginas, capa=None):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
        self.capa = capa

    def __str__(self):
        return f"'{self.titulo}' - {self.autor} ({self.paginas} páginas)"

    def __repr__(self):
        return f"Livro(id={self.id_livro}, titulo='{self.titulo}')"