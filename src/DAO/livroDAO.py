from .dao import BaseDAO


class LivroDAO(BaseDAO):
    """DAO para gerenciar livros"""

    def inserir(self, livro):
        """Insere um novo livro"""
        try:
            query = """
            INSERT INTO livro 
            (titulo, autor, paginas, capa)
            VALUES (?, ?, ?, ?)
            """
            params = (livro.titulo, livro.autor, livro.paginas, livro.capa)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir livro: {e}")
            return None

    def listar(self):
        """Lista todos os livros"""
        try:
            query = "SELECT * FROM livro"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
            return []

    def listar_por_id(self, id_livro):
        """Lista um livro por ID"""
        try:
            query = "SELECT * FROM livro WHERE id_livro = ?"
            self.cursor.execute(query, (id_livro,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar livro: {e}")
            return None

    def listar_por_autor(self, autor):
        """Lista livros de um autor"""
        try:
            query = "SELECT * FROM livro WHERE autor = ?"
            self.cursor.execute(query, (autor,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar livros por autor: {e}")
            return []

    def listar_por_titulo(self, titulo):
        """Lista livros por título (busca parcial)"""
        try:
            query = "SELECT * FROM livro WHERE titulo LIKE ?"
            self.cursor.execute(query, (f"%{titulo}%",))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar livros por título: {e}")
            return []

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
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar livro: {e}")
            return False

    def excluir(self, id_livro):
        """Exclui um livro"""
        try:
            query = "DELETE FROM livro WHERE id_livro = ?"
            self.cursor.execute(query, (id_livro,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir livro: {e}")
            return False
