from .dao import BaseDAO


class EmprestimoDAO(BaseDAO):
    """DAO para gerenciar empréstimos de livros"""

    def inserir(self, emprestimo):
        """Insere um novo empréstimo"""
        try:
            query = """
            INSERT INTO emprestimo 
            (id_exemplar, id_dono, id_emprestado, data_inicio, data_prevista, data_devolucao)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (emprestimo.id_exemplar, emprestimo.id_dono, emprestimo.id_emprestado,
                      emprestimo.data_inicio, emprestimo.data_prevista, emprestimo.data_devolucao)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir empréstimo: {e}")
            return None

    def listar(self):
        """Lista todos os empréstimos"""
        try:
            query = "SELECT * FROM emprestimo"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar empréstimos: {e}")
            return []

    def listar_por_id(self, id_emprestimo):
        """Lista um empréstimo por ID"""
        try:
            query = "SELECT * FROM emprestimo WHERE id_emprestimo = ?"
            self.cursor.execute(query, (id_emprestimo,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar empréstimo: {e}")
            return None

    def atualizar(self, emprestimo):
        """Atualiza um empréstimo existente"""
        try:
            query = """
            UPDATE emprestimo 
            SET id_exemplar = ?, id_dono = ?, id_emprestado = ?, 
                data_inicio = ?, data_prevista = ?, data_devolucao = ?
            WHERE id_emprestimo = ?
            """
            params = (emprestimo.id_exemplar, emprestimo.id_dono, emprestimo.id_emprestado,
                      emprestimo.data_inicio, emprestimo.data_prevista, 
                      emprestimo.data_devolucao, emprestimo.id_emprestimo)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar empréstimo: {e}")
            return False

    def excluir(self, id_emprestimo):
        """Exclui um empréstimo"""
        try:
            query = "DELETE FROM emprestimo WHERE id_emprestimo = ?"
            self.cursor.execute(query, (id_emprestimo,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir empréstimo: {e}")
            return False