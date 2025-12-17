"""
Modelo de Avaliação de Usuário - Implementa encapsulamento com propriedades
"""
from exceptions import AvaliacaoException
from datetime import datetime


class AvaliacaoUsuario:
    """
    Modelo de avaliação de usuário do sistema.
    Implementa encapsulamento de atributos com validação.
    """
    
    NOTA_MINIMA = 1
    NOTA_MAXIMA = 5
    
    def __init__(self, id_avaliacao, id_avaliador, id_avaliado, nota, comentario, data_avaliacao):
        """
        Inicializa uma nova avaliação
        
        Args:
            id_avaliacao: ID único da avaliação
            id_avaliador: ID do usuário que avalia
            id_avaliado: ID do usuário sendo avaliado
            nota: Nota de 1 a 5
            comentario: Comentário da avaliação
            data_avaliacao: Data da avaliação
            
        Raises:
            AvaliacaoException.AvaliacaoInvalida: Se dados inválidos
        """
        self._id_avaliacao = id_avaliacao
        self._id_avaliador = id_avaliador
        self._id_avaliado = id_avaliado
        self.nota = nota  # Usa property
        self.comentario = comentario  # Usa property
        self.data_avaliacao = data_avaliacao  # Usa property

    @property
    def id_avaliacao(self):
        """Getter do ID da avaliação"""
        return self._id_avaliacao

    @property
    def id_avaliador(self):
        """Getter do ID do avaliador"""
        return self._id_avaliador

    @property
    def id_avaliado(self):
        """Getter do ID do avaliado"""
        return self._id_avaliado

    @property
    def nota(self):
        """Getter da nota"""
        return self._nota
    
    @nota.setter
    def nota(self, value):
        """Setter com validação da nota"""
        valor_int = int(value)
        if valor_int < self.NOTA_MINIMA or valor_int > self.NOTA_MAXIMA:
            raise AvaliacaoException.AvaliacaoInvalida(
                f"Nota deve estar entre {self.NOTA_MINIMA} e {self.NOTA_MAXIMA}"
            )
        self._nota = valor_int

    @property
    def comentario(self):
        """Getter do comentário"""
        return self._comentario
    
    @comentario.setter
    def comentario(self, value):
        """Setter com validação do comentário"""
        if value and len(value.strip()) > 500:
            raise AvaliacaoException.AvaliacaoInvalida(
                "Comentário não pode exceder 500 caracteres"
            )
        self._comentario = value.strip() if value else ""

    @property
    def data_avaliacao(self):
        """Getter da data da avaliação"""
        return self._data_avaliacao
    
    @data_avaliacao.setter
    def data_avaliacao(self, value):
        """Setter com validação da data"""
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise AvaliacaoException.AvaliacaoInvalida(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )
        self._data_avaliacao = value

    def __str__(self):
        """Representação em string da avaliação"""
        return f"Avaliação: {self.nota}/5 - '{self.comentario[:30]}...'"

    def __repr__(self):
        """Representação técnica da avaliação"""
        return f"AvaliacaoUsuario(id={self.id_avaliacao}, nota={self.nota})"

    def __eq__(self, other):
        """Compara avaliações por ID"""
        if not isinstance(other, AvaliacaoUsuario):
            return False
        return self.id_avaliacao == other.id_avaliacao
