from .dao import BaseDAO


class HistoricoEmprestimosDAO(BaseDAO):
    """DAO para gerenciar histórico de empréstimos"""

    def inserir(self, historico):
        """Insere um novo registro de histórico"""
        try:
            query = """
            INSERT INTO historico_emprestimos 
            (id_emprestimo, status_final)
            VALUES (?, ?)
            """
            params = (historico.id_emprestimo, historico.status_final)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir histórico: {e}")
            return None

    def listar(self):
        """Lista todo o histórico"""
        try:
            query = "SELECT * FROM historico_emprestimos"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar histórico: {e}")
            return []

    def listar_por_id(self, id_historico):
        """Lista um registro de histórico por ID"""
        try:
            query = "SELECT * FROM historico_emprestimos WHERE id_historico = ?"
            self.cursor.execute(query, (id_historico,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return None

    def atualizar(self, historico):
        """Atualiza um registro de histórico"""
        try:
            query = """
            UPDATE historico_emprestimos 
            SET id_emprestimo = ?, status_final = ?
            WHERE id_historico = ?
            """
            params = (historico.id_emprestimo, historico.status_final, historico.id_historico)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar histórico: {e}")
            return False

    def excluir(self, id_historico):
        """Exclui um registro de histórico"""
        try:
            query = "DELETE FROM historico_emprestimos WHERE id_historico = ?"
            self.cursor.execute(query, (id_historico,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir histórico: {e}")
            return False