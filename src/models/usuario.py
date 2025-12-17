"""
Modelo de Usuário - Implementa encapsulamento com propriedades
"""
from exceptions import UsuarioException


class Usuario:
    """Modelo de usuário do sistema"""
    
    def __init__(self, id_usuario, username, senha, email, idade):
        """
        Inicializa um novo usuário
        
        Args:
            id_usuario: ID único do usuário
            username: Nome de usuário (único)
            senha: Senha do usuário
            email: Email do usuário (único)
            idade: Idade do usuário
            
        Raises:
            UsuarioException.DadosInvalidos: Se dados inválidos
        """
        self._id_usuario = id_usuario
        self.username = username  # Usa property
        self.senha = senha  # Usa property
        self.email = email  # Usa property
        self.idade = idade  # Usa property

    @property
    def id_usuario(self):
        """Getter do ID do usuário"""
        return self._id_usuario

    @property
    def username(self):
        """Getter do username"""
        return self._username
    
    @username.setter
    def username(self, value):
        """Setter com validação do username"""
        if not value or len(value.strip()) < 3:
            raise UsuarioException.DadosInvalidos(
                "Username deve ter pelo menos 3 caracteres"
            )
        self._username = value.strip()

    @property
    def senha(self):
        """Getter da senha"""
        return self._senha
    
    @senha.setter
    def senha(self, value):
        """Setter com validação da senha"""
        if not value or len(value) < 6:
            raise UsuarioException.DadosInvalidos(
                "Senha deve ter pelo menos 6 caracteres"
            )
        self._senha = value

    @property
    def email(self):
        """Getter do email"""
        return self._email
    
    @email.setter
    def email(self, value):
        """Setter com validação do email"""
        if "@" not in value or "." not in value:
            raise UsuarioException.DadosInvalidos(
                "Email inválido"
            )
        self._email = value.lower()

    @property
    def idade(self):
        """Getter da idade"""
        return self._idade
    
    @idade.setter
    def idade(self, value):
        """Setter com validação da idade"""
        if value < 13 or value > 120:
            raise UsuarioException.DadosInvalidos(
                "Idade deve estar entre 13 e 120 anos"
            )
        self._idade = int(value)

    def __str__(self):
        """Representação em string do usuário"""
        return f"{self.username} - {self.idade} anos ({self.email})"

    def __repr__(self):
        """Representação técnica do usuário"""
        return f"Usuario(id={self.id_usuario}, username='{self.username}')"

    def __eq__(self, other):
        """Compara usuários por ID"""
        if not isinstance(other, Usuario):
            return False
        return self.id_usuario == other.id_usuario
