"""
Modelo de Livro - Implementa encapsulamento com propriedades
"""
from exceptions import LivroException


class Livro:
    """
    Modelo de livro do sistema.
    Implementa encapsulamento de atributos com validação.
    """
    
    def __init__(self, id_livro, titulo, autor, paginas, capa=None):
        """
        Inicializa um novo livro
        
        Args:
            id_livro: ID único do livro
            titulo: Título do livro
            autor: Autor do livro
            paginas: Número de páginas
            capa: URL ou caminho da imagem da capa
            
        Raises:
            LivroException.DadosInvalidos: Se dados inválidos
        """
        self._id_livro = id_livro
        self.titulo = titulo  # Usa property
        self.autor = autor  # Usa property
        self.paginas = paginas  # Usa property
        self.capa = capa  # Usa property

    @property
    def id_livro(self):
        """Getter do ID do livro"""
        return self._id_livro

    @property
    def titulo(self):
        """Getter do título"""
        return self._titulo
    
    @titulo.setter
    def titulo(self, value):
        """Setter com validação do título"""
        if not value or len(value.strip()) < 1:
            raise LivroException.DadosInvalidos("Título não pode estar vazio")
        self._titulo = value.strip()

    @property
    def autor(self):
        """Getter do autor"""
        return self._autor
    
    @autor.setter
    def autor(self, value):
        """Setter com validação do autor"""
        if not value or len(value.strip()) < 1:
            raise LivroException.DadosInvalidos("Autor não pode estar vazio")
        self._autor = value.strip()

    @property
    def paginas(self):
        """Getter do número de páginas"""
        return self._paginas
    
    @paginas.setter
    def paginas(self, value):
        """Setter com validação de páginas"""
        if value < 1:
            raise LivroException.DadosInvalidos("Livro deve ter pelo menos 1 página")
        self._paginas = int(value)

    @property
    def capa(self):
        """Getter da capa"""
        return self._capa
    
    @capa.setter
    def capa(self, value):
        """Setter da capa"""
        self._capa = value

    def __str__(self):
        """Representação em string do livro"""
        return f"'{self.titulo}' - {self.autor} ({self.paginas}p)"

    def __repr__(self):
        """Representação técnica do livro"""
        return f"Livro(id={self.id_livro}, titulo='{self.titulo}')"

    def __eq__(self, other):
        """Compara livros por ID"""
        if not isinstance(other, Livro):
            return False
        return self.id_livro == other.id_livro
