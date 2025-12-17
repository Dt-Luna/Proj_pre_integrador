"""
Modelo de Exemplar - Implementa encapsulamento com propriedades
"""
from exceptions import ExemplarException


class Exemplar:
    """
    Modelo de exemplar de livro do sistema.
    Implementa encapsulamento de atributos com validação.
    """
    
    STATUS_DISPONIVEL = "disponível"
    STATUS_EMPRESTADO = "emprestado"
    STATUS_RESERVADO = "reservado"
    STATUSES_VALIDOS = [STATUS_DISPONIVEL, STATUS_EMPRESTADO, STATUS_RESERVADO]
    
    def __init__(self, id_exemplar, id_usuario, id_livro, status=STATUS_DISPONIVEL):
        """
        Inicializa um novo exemplar
        
        Args:
            id_exemplar: ID único do exemplar
            id_usuario: ID do usuário dono do exemplar
            id_livro: ID do livro
            status: Status do exemplar (disponível, emprestado, reservado)
            
        Raises:
            ExemplarException.DadosInvalidos: Se dados inválidos
        """
        self._id_exemplar = id_exemplar
        self._id_usuario = id_usuario
        self._id_livro = id_livro
        self.status = status  # Usa property

    @property
    def id_exemplar(self):
        """Getter do ID do exemplar"""
        return self._id_exemplar

    @property
    def id_usuario(self):
        """Getter do ID do usuário"""
        return self._id_usuario

    @property
    def id_livro(self):
        """Getter do ID do livro"""
        return self._id_livro

    @property
    def status(self):
        """Getter do status"""
        return self._status
    
    @status.setter
    def status(self, value):
        """Setter com validação do status"""
        if value not in self.STATUSES_VALIDOS:
            raise ExemplarException.DadosInvalidos(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status = value

    def esta_disponivel(self):
        """Verifica se o exemplar está disponível"""
        return self.status == self.STATUS_DISPONIVEL

    def emprestar(self):
        """Marca o exemplar como emprestado"""
        if not self.esta_disponivel():
            raise ExemplarException.ExemplarIndisponivel(
                f"Exemplar não está disponível (status: {self.status})"
            )
        self.status = self.STATUS_EMPRESTADO

    def devolver(self):
        """Marca o exemplar como devolvido"""
        self.status = self.STATUS_DISPONIVEL

    def reservar(self):
        """Marca o exemplar como reservado"""
        if self.status == self.STATUS_EMPRESTADO:
            self.status = self.STATUS_RESERVADO
        elif not self.esta_disponivel():
            raise ExemplarException.ExemplarIndisponivel(
                f"Não é possível reservar exemplar com status: {self.status}"
            )

    def __str__(self):
        """Representação em string do exemplar"""
        return f"Exemplar({self.id_exemplar}) - Livro:{self.id_livro} - {self.status}"

    def __repr__(self):
        """Representação técnica do exemplar"""
        return f"Exemplar(id={self.id_exemplar}, livro={self.id_livro})"

    def __eq__(self, other):
        """Compara exemplares por ID"""
        if not isinstance(other, Exemplar):
            return False
        return self.id_exemplar == other.id_exemplar
