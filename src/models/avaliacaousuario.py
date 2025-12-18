from exceptions import AvaliacaoException
from datetime import datetime


class AvaliacaoUsuario:
    
    NOTA_MINIMA = 1
    NOTA_MAXIMA = 5
    
    def __init__(self, id_avaliacao, id_avaliador, id_avaliado, nota, comentario, data_avaliacao):
        self._id_avaliacao = id_avaliacao
        self._id_avaliador = id_avaliador
        self._id_avaliado = id_avaliado
        self.nota = nota 
        self.comentario = comentario  
        self.data_avaliacao = data_avaliacao  

    @property
    def id_avaliacao(self):
        return self._id_avaliacao

    @property
    def id_avaliador(self):
        return self._id_avaliador

    @property
    def id_avaliado(self):
        return self._id_avaliado

    @property
    def nota(self):
        return self._nota
    
    @nota.setter
    def nota(self, value):
        valor_int = int(value)
        if valor_int < self.NOTA_MINIMA or valor_int > self.NOTA_MAXIMA:
            raise AvaliacaoException.AvaliacaoInvalida(
                f"Nota deve estar entre {self.NOTA_MINIMA} e {self.NOTA_MAXIMA}"
            )
        self._nota = valor_int

    @property
    def comentario(self):
        return self._comentario
    
    @comentario.setter
    def comentario(self, value):
        if value and len(value.strip()) > 500:
            raise AvaliacaoException.AvaliacaoInvalida(
                "Comentário não pode exceder 500 caracteres"
            )
        self._comentario = value.strip() if value else ""

    @property
    def data_avaliacao(self):
        return self._data_avaliacao
    
    @data_avaliacao.setter
    def data_avaliacao(self, value):
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise AvaliacaoException.AvaliacaoInvalida(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )
        self._data_avaliacao = value

    def __str__(self):
        return f"Avaliação: {self.nota}/5 - '{self.comentario[:30]}...'"

    def __repr__(self):
        """Representação técnica da avaliação"""
        return f"AvaliacaoUsuario(id={self.id_avaliacao}, nota={self.nota})"

    def __eq__(self, other):
        """Compara avaliações por ID"""
        if not isinstance(other, AvaliacaoUsuario):
            return False
        return self.id_avaliacao == other.id_avaliacao
