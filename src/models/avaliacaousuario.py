class AvaliacaoUsuario:
    """Modelo de avaliação de usuário"""
    
    def __init__(self, id_avaliacao, id_avaliador, id_avaliado, nota, comentario, data_avaliacao):
        self.id_avaliacao = id_avaliacao
        self.id_avaliador = id_avaliador
        self.id_avaliado = id_avaliado
        self.nota = nota
        self.comentario = comentario
        self.data_avaliacao = data_avaliacao

    def __str__(self):
        return f"Avaliação: {self.nota}/5 - '{self.comentario[:30]}...'"

    def __repr__(self):
        return f"AvaliacaoUsuario(id={self.id_avaliacao}, nota={self.nota})"