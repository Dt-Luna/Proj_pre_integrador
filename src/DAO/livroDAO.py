from .dao import BaseDAO
from models.livro import Livro
from exceptions import LivroException, DAOException


class LivroDAO(BaseDAO):
    """DAO para gerenciar livros - Herda de BaseDAO"""

    def inserir(self, livro):
        """Insere um novo livro"""
        try:
            query = """
            INSERT INTO livro 
            (titulo, autor, paginas, capa)
            VALUES (?, ?, ?, ?)
            """
            params = (livro.titulo, livro.autor, livro.paginas, livro.capa)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir livro: {str(e)}")

    def listar(self):
        """Lista todos os livros"""
        try:
            query = "SELECT * FROM livro"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar livros: {str(e)}")

    def listar_por_id(self, id_livro):
        """Lista um livro por ID"""
        try:
            query = "SELECT * FROM livro WHERE id_livro = ?"
            resultado = self._executar_query(query, (id_livro,), fetch_one=True)
            if not resultado:
                raise LivroException.LivroNaoEncontrado(f"Livro {id_livro} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar livro: {str(e)}")

    def listar_por_autor(self, autor):
        """Lista livros de um autor"""
        try:
            query = "SELECT * FROM livro WHERE autor = ?"
            return self._executar_query(query, (autor,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar livros por autor: {str(e)}")

    def listar_por_titulo(self, titulo):
        """Lista livros por título (busca parcial)"""
        try:
            query = "SELECT * FROM livro WHERE titulo LIKE ?"
            return self._executar_query(query, (f"%{titulo}%",), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar livros por título: {str(e)}")

    def atualizar(self, livro):
        """Atualiza um livro existente"""
        try:
            query = """
            UPDATE livro 
            SET titulo = ?, autor = ?, paginas = ?, capa = ?
            WHERE id_livro = ?
            """
            params = (livro.titulo, livro.autor, livro.paginas, 
                      livro.capa, livro.id_livro)
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar livro: {str(e)}")

    def excluir(self, id_livro):
        """Exclui um livro"""
        try:
            query = "DELETE FROM livro WHERE id_livro = ?"
            return self._executar_query(query, (id_livro,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir livro: {str(e)}")
