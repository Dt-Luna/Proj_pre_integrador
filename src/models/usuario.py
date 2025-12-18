from exceptions import UsuarioException


class Usuario:
    
    def __init__(self, id_usuario, username, senha, email, idade):
        self._id_usuario = id_usuario
        self.username = username  
        self.senha = senha  
        self.email = email 
        self.idade = idade  

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if not value or len(value.strip()) < 3:
            raise UsuarioException.DadosInvalidos(
                "Username deve ter pelo menos 3 caracteres"
            )
        self._username = value.strip()

    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, value):
        if not value or len(value) < 6:
            raise UsuarioException.DadosInvalidos(
                "Senha deve ter pelo menos 6 caracteres"
            )
        self._senha = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise UsuarioException.DadosInvalidos(
                "Email inválido"
            )
        self._email = value.lower()

    @property
    def idade(self):
        return self._idade
    
    @idade.setter
    def idade(self, value):
        if value < 18 or value > 120:
            raise UsuarioException.DadosInvalidos(
                "Idade deve estar entre 18 e 120 anos"
            )
        self._idade = int(value)

    def __str__(self):
        return f"{self.username} - {self.idade} anos ({self.email})"

    def __repr__(self):
        """Representação técnica do usuário"""
        return f"Usuario(id={self.id_usuario}, username='{self.username}')"

    def __eq__(self, other):
        """Compara usuários por ID"""
        if not isinstance(other, Usuario):
            return False
        return self.id_usuario == other.id_usuario
