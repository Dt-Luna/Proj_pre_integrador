class Exemplar:
    def __init__(self, id_exemplar, email_cliente, id_livro, status_exemplar):
        self.set_id_exemplar(id_exemplar)
        self.set_email_cliente(email_cliente)
        self.set_id_livro(id_livro)
        self.set_status_exemplar(status_exemplar)
    def set_id_exemplar(self, id):
        self.__id_exemplar = id
    def set_email_cliente(self, email):
        self.__email_cliente = email
    def set_id_livro(self, id):
        self.__id_livro = id
    def set_status_exemplar(self, status):
        self.__status_exemplar = status
    def get_id_exemplar(self): return self.__id_exemplar
    def get_email_cliente(self): return self.__email_cliente
    def get_id_livro(self): return self.__id_livro
    def get_status_exemplar(self): return self.__status_exemplar
    def __str__(self): f"{self.__email_cliente} - {self.__id_livro} - {self.__id_exemplar} - {self.__status_exemplar}"