class Usuario:
    """Modelo de usuário do sistema"""
    
    def __init__(self, id_usuario, email, username, senha, idade):
        self.id_usuario = id_usuario
        self.email = email
        self.username = username
        self.senha = senha
        self.idade = idade

    def __str__(self):
        return f"{self.username} - {self.idade} anos - {self.email}"

    def __repr__(self):
        return f"Usuario(id={self.id_usuario}, username='{self.username}')"