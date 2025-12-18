from exceptions import LivroException


class Livro:
    
    def __init__(self, id_livro, titulo, autor, paginas, capa=None):
        self._id_livro = id_livro
        self.titulo = titulo  
        self.autor = autor  
        self.paginas = paginas  
        self.capa = capa  

    @property
    def id_livro(self):
        return self._id_livro

    @property
    def titulo(self):
        return self._titulo
    
    @titulo.setter
    def titulo(self, value):
        if not value or len(value.strip()) < 1:
            raise LivroException.DadosInvalidos("Título não pode estar vazio")
        self._titulo = value.strip()

    @property
    def autor(self):
        return self._autor
    
    @autor.setter
    def autor(self, value):
        if not value or len(value.strip()) < 1:
            raise LivroException.DadosInvalidos("Autor não pode estar vazio")
        self._autor = value.strip()

    @property
    def paginas(self):
        return self._paginas
    
    @paginas.setter
    def paginas(self, value):
        if value < 1:
            raise LivroException.DadosInvalidos("Livro deve ter pelo menos 1 página")
        self._paginas = int(value)

    @property
    def capa(self):
        return self._capa
    
    @capa.setter
    def capa(self, value):
        self._capa = value

    def __str__(self):
        return f"'{self.titulo}' - {self.autor} ({self.paginas}p)"

    def __repr__(self):
        """Representação técnica do livro"""
        return f"Livro(id={self.id_livro}, titulo='{self.titulo}')"

    def __eq__(self, other):
        """Compara livros por ID"""
        if not isinstance(other, Livro):
            return False
        return self.id_livro == other.id_livro
