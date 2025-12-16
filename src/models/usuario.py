class Usuario:
    def __init__(self, email, username, senha, idade):
        self.set_email(email)
        self.set_username(username)
        self.set_senha(senha)
        self.set_idade(idade)
    def set_email(self,email):
        self.__email = email
    def set_username(self, username):
        self.__username = username
    def set_senha(self, senha):
        self.__senha = senha
    def set_idade(self, idade):
        self.__idade = idade
    def get_idade(self): return self.__idade
    def get_senha(self): return self.__senha
    def get_username(self): return self.__username
    def get_email(self): return self.__email
    def __str__(self): f"{self.__username} - {self.__idade} - {self.__email}"