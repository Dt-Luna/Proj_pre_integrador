from .dao import BaseDAO


class AvaliacaoUsuarioDAO(BaseDAO):
    """DAO para gerenciar avaliações de usuários"""

    def inserir(self, avaliacao):
        """Insere uma nova avaliação de usuário"""
        try:
            query = """
            INSERT INTO avaliacao_usuario 
            (id_avaliador, id_avaliado, nota, comentario, data_avaliacao)
            VALUES (?, ?, ?, ?, ?)
            """
            params = (avaliacao.id_avaliador, avaliacao.id_avaliado, 
                      avaliacao.nota, avaliacao.comentario, avaliacao.data_avaliacao)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir avaliação: {e}")
            return None

    def listar(self):
        """Lista todas as avaliações"""
        try:
            query = "SELECT * FROM avaliacao_usuario"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar avaliações: {e}")
            return []

    def listar_por_id(self, id_avaliacao):
        """Lista uma avaliação por ID"""
        try:
            query = "SELECT * FROM avaliacao_usuario WHERE id_avaliacao = ?"
            self.cursor.execute(query, (id_avaliacao,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar avaliação: {e}")
            return None

    def atualizar(self, avaliacao):
        """Atualiza uma avaliação existente"""
        try:
            query = """
            UPDATE avaliacao_usuario 
            SET id_avaliador = ?, id_avaliado = ?, nota = ?, 
                comentario = ?, data_avaliacao = ?
            WHERE id_avaliacao = ?
            """
            params = (avaliacao.id_avaliador, avaliacao.id_avaliado,
                      avaliacao.nota, avaliacao.comentario, 
                      avaliacao.data_avaliacao, avaliacao.id_avaliacao)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar avaliação: {e}")
            return False

    def excluir(self, id_avaliacao):
        """Exclui uma avaliação"""
        try:
            query = "DELETE FROM avaliacao_usuario WHERE id_avaliacao = ?"
            self.cursor.execute(query, (id_avaliacao,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir avaliação: {e}")
            return False