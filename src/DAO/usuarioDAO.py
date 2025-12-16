from .dao import BaseDAO


class UsuarioDAO(BaseDAO):
    """DAO para gerenciar usuários"""

    def inserir(self, usuario):
        """Insere um novo usuário"""
        try:
            query = """
            INSERT INTO usuario 
            (username, senha, idade, email)
            VALUES (?, ?, ?, ?)
            """
            params = (usuario.username, usuario.senha, usuario.idade, usuario.email)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir usuário: {e}")
            return None

    def listar(self):
        """Lista todos os usuários"""
        try:
            query = "SELECT * FROM usuario"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    def listar_por_id(self, id_usuario):
        """Lista um usuário por ID"""
        try:
            query = "SELECT * FROM usuario WHERE id_usuario = ?"
            self.cursor.execute(query, (id_usuario,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def listar_por_email(self, email):
        """Lista um usuário por email"""
        try:
            query = "SELECT * FROM usuario WHERE email = ?"
            self.cursor.execute(query, (email,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar usuário por email: {e}")
            return None

    def listar_por_username(self, username):
        """Lista um usuário por username"""
        try:
            query = "SELECT * FROM usuario WHERE username = ?"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar usuário por username: {e}")
            return None

    def atualizar(self, usuario):
        """Atualiza um usuário existente"""
        try:
            query = """
            UPDATE usuario 
            SET username = ?, senha = ?, idade = ?, email = ?
            WHERE id_usuario = ?
            """
            params = (usuario.username, usuario.senha, usuario.idade, 
                      usuario.email, usuario.id_usuario)
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao atualizar usuário: {e}")
            return False

    def excluir(self, id_usuario):
        """Exclui um usuário"""
        try:
            query = "DELETE FROM usuario WHERE id_usuario = ?"
            self.cursor.execute(query, (id_usuario,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao excluir usuário: {e}")
            return False
