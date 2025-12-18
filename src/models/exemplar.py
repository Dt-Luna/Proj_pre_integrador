from exceptions import ExemplarException


class Exemplar:
    
    STATUS_DISPONIVEL = "disponível"
    STATUS_EMPRESTADO = "emprestado"
    STATUS_RESERVADO = "reservado"
    STATUSES_VALIDOS = [STATUS_DISPONIVEL, STATUS_EMPRESTADO, STATUS_RESERVADO]
    
    def __init__(self, id_exemplar, id_usuario, id_livro, status=STATUS_DISPONIVEL):
        self._id_exemplar = id_exemplar
        self._id_usuario = id_usuario
        self._id_livro = id_livro
        self.status = status  

    @property
    def id_exemplar(self):
        return self._id_exemplar

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_livro(self):
        return self._id_livro

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if value not in self.STATUSES_VALIDOS:
            raise ExemplarException.DadosInvalidos(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status = value

    def esta_disponivel(self):
        return self.status == self.STATUS_DISPONIVEL

    def emprestar(self):
        if not self.esta_disponivel():
            raise ExemplarException.ExemplarIndisponivel(
                f"Exemplar não está disponível (status: {self.status})"
            )
        self.status = self.STATUS_EMPRESTADO

    def devolver(self):
        self.status = self.STATUS_DISPONIVEL

    def reservar(self):
        if self.status == self.STATUS_EMPRESTADO:
            self.status = self.STATUS_RESERVADO
        elif not self.esta_disponivel():
            raise ExemplarException.ExemplarIndisponivel(
                f"Não é possível reservar exemplar com status: {self.status}"
            )

    def __str__(self):
        return f"Exemplar({self.id_exemplar}) - Livro:{self.id_livro} - {self.status}"

    def __repr__(self):
        """Representação técnica do exemplar"""
        return f"Exemplar(id={self.id_exemplar}, livro={self.id_livro})"

    def __eq__(self, other):
        """Compara exemplares por ID"""
        if not isinstance(other, Exemplar):
            return False
        return self.id_exemplar == other.id_exemplar
