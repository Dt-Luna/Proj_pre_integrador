from exceptions import LivroException, DAOException
from .dao import BaseDAO


class Livro:
    
    def __init__(self, id_livro, titulo, autor, paginas, isbn):
        self._id_livro = id_livro
        self._titulo = None
        self._autor = None
        self._paginas = None
        self._isbn = None
        
        self.set_titulo(titulo)
        self.set_autor(autor)
        self.set_paginas(paginas)
        self.set_isbn(isbn)

    def get_id(self):
        return self._id_livro
    
    def set_id(self, id_livro):
        self._id_livro = id_livro

    def get_titulo(self):
        return self._titulo
    
    def set_titulo(self, value):
        if not value or len(value.strip()) < 1:
            raise LivroException.DadosInvalidos("Título não pode estar vazio")
        self._titulo = value.strip()

    def get_autor(self):
        return self._autor
    
    def set_autor(self, value):
        if not value or len(value.strip()) < 1:
            raise LivroException.DadosInvalidos("Autor não pode estar vazio")
        self._autor = value.strip()

    def get_paginas(self):
        return self._paginas
    
    def set_paginas(self, value):
        if value < 1:
            raise LivroException.DadosInvalidos("Livro deve ter pelo menos 1 página")
        self._paginas = int(value)

    def get_capa(self):
        return self._capa

    def get_isbn(self):
        return self._isbn

    def set_isbn(self, value):
        if not value or len(value.strip()) < 10:
            raise LivroException.DadosInvalidos("ISBN inválido")
        self._isbn = value.strip()

    def __str__(self):
        return f"'{self.get_titulo()}' - {self.get_autor()} ({self.get_paginas()}p)"

    def __repr__(self):
        return f"Livro(id={self.get_id()}, titulo='{self.get_titulo()}')"

    def __eq__(self, other):
        if not isinstance(other, Livro):
            return False
        return self.get_id() == other.get_id()


class LivroDAO(BaseDAO):

    def inserir(self, livro):
        try:
            query = """
            INSERT INTO livro 
            (titulo, autor, paginas, isbn)
            VALUES (?, ?, ?, ?)
            """
            params = (livro.get_titulo(), livro.get_autor(), 
                     livro.get_paginas(), livro.get_isbn(),)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir livro: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM livro ORDER BY titulo ASC"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar livros: {str(e)}")

    def listar_id(self, id_livro):
        try:
            query = "SELECT * FROM livro WHERE id_livro = ?"
            resultado = self._executar_query(query, (id_livro,), fetch_one=True)
            if not resultado:
                raise LivroException.LivroNaoEncontrado(f"Livro {id_livro} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar livro: {str(e)}")

    def listar_por_autor(self, autor):
        try:
            query = "SELECT * FROM livro WHERE autor = ?"
            return self._executar_query(query, (autor,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar livros por autor: {str(e)}")

    def listar_por_titulo(self, titulo):
        try:
            query = "SELECT * FROM livro WHERE titulo LIKE ?"
            return self._executar_query(query, (f"%{titulo}%",), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar livros por título: {str(e)}")

    def atualizar(self, livro):
        try:
            query = """
            UPDATE livro 
            SET titulo = ?, autor = ?, paginas = ?, isbn = ?
            WHERE id_livro = ?
            """
            params = (livro.get_titulo(), livro.get_autor(), livro.get_paginas(), 
                     livro.get_isbn(), livro.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar livro: {str(e)}")

    def excluir(self, id_livro):
        try:
            query = "DELETE FROM livro WHERE id_livro = ?"
            return self._executar_query(query, (id_livro,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir livro: {str(e)}")
    