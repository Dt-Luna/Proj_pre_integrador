from .dao import BaseDAO


class ExemplarDAO(BaseDAO):
    """DAO para gerenciar exemplares de livros"""

    def inserir(self, exemplar):
        """Insere um novo exemplar"""
        try:
            query = """
            INSERT INTO exemplar 
            (id_usuario, id_livro, status)
            VALUES (?, ?, ?)
            """
            params = (exemplar.id_usuario, exemplar.id_livro, exemplar.status)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir exemplar: {e}")
            return None

    def listar(self):
        """Lista todos os exemplares"""
        try:
            query = "SELECT * FROM exemplar"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar exemplares: {e}")
            return []

    def listar_por_id(self, id_exemplar):
        """Lista um exemplar por ID"""
        try:
            query = "SELECT * FROM exemplar WHERE id_exemplar = ?"
            self.cursor.execute(query, (id_exemplar,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar exemplar: {e}")
            return None

    def listar_por_usuario(self, id_usuario):
        """Lista exemplares de um usuário"""
        try:
            query = "SELECT * FROM exemplar WHERE id_usuario = ?"
            self.cursor.execute(query, (id_usuario,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar exemplares do usuário: {e}")
            return []

    def listar_por_livro(self, id_livro):
        """Lista exemplares de um livro"""
        try:
            query = "SELECT * FROM exemplar WHERE id_livro = ?"
            self.cursor.execute(query, (id_livro,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar exemplares do livro: {e}")
            return []

    def listar_por_status(self, status):
        """Lista exemplares por status"""
        try:
            query = "SELECT * FROM exemplar WHERE status = ?"
            self.cursor.execute(query, (status,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar exemplares por status: {e}")
            return []

    def atualizar(self, exemplar):
        """Atualiza um exemplar existente"""
        try:
            query = """
            UPDATE exemplar 
            SET id_usuario = ?, id_livro = ?, status = ?
            WHERE id_exemplar = ?
            """
            params = (exemplar.id_usuario, exemplar.id_livro, 
                      exemplar.status, exemplar.id_exemplar)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar exemplar: {e}")
            return False

    def excluir(self, id_exemplar):
        """Exclui um exemplar"""
        try:
            query = "DELETE FROM exemplar WHERE id_exemplar = ?"
            self.cursor.execute(query, (id_exemplar,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir exemplar: {e}")
            return False
