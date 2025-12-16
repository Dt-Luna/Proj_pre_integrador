class Livro:
    def __init__(self, id_livro, titulo, autor, paginas, capa):
        self.set_id_livro(id_livro)
        self.set_titulo(titulo)
        self.set_autor(autor)
        self.set_paginas(paginas)
        self.set_capa(capa)
    def set_id_livro(self, id):
        self.__id_livro = id
    def set_titulo(self, titulo):
        self.__titulo = titulo
    def set_autor(self, autor):
        self.__autor = autor
    def set_paginas(self, paginas):
        self.__paginas = paginas
    def set_capa(self, capa):
        self.__capa = capa
    def get_capa(self): return self.__capa
    def get_paginas(self): return self.__paginas
    def get_autor(self): return self.__autor
    def get_titulo(self): return self.__titulo
    def get_id_livro(self): return self.__id_livro
    def __str__(self): f"{self.__id_livro} - {self.__titulo} - {self.__autor} - {self.__paginas}"