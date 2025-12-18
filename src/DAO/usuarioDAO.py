from .dao import BaseDAO
from models.usuario import Usuario
from exceptions import UsuarioException, DAOException


class UsuarioDAO(BaseDAO):

    def inserir(self, usuario):
        try:
            query = """
            INSERT INTO usuario 
            (username, senha, idade, email)
            VALUES (?, ?, ?, ?)
            """
            params = (usuario.username, usuario.senha, usuario.idade, usuario.email)
            return self._executar_query(query, params)
        except DAOException.OperacaoFalhou as e:
            if "UNIQUE constraint failed" in str(e):
                raise UsuarioException.UsuarioDuplicado(
                    "Username ou email já registrado"
                )
            raise
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir usuário: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM usuario"
            return self._executar_query(query, fetch=True) or []
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar usuários: {str(e)}")

    def listar_por_id(self, id_usuario):
        try:
            query = "SELECT * FROM usuario WHERE id_usuario = ?"
            resultado = self._executar_query(query, (id_usuario,), fetch_one=True)
            if not resultado:
                raise UsuarioException.UsuarioNaoEncontrado(
                    f"Usuário {id_usuario} não encontrado"
                )
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar usuário: {str(e)}")

    def listar_por_email(self, email):
        try:
            query = "SELECT * FROM usuario WHERE email = ?"
            return self._executar_query(query, (email,), fetch_one=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(
                f"Erro ao buscar usuário por email: {str(e)}"
            )

    def listar_por_username(self, username):
        try:
            query = "SELECT * FROM usuario WHERE username = ?"
            return self._executar_query(query, (username,), fetch_one=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(
                f"Erro ao buscar usuário por username: {str(e)}"
            )

    def atualizar(self, usuario):
        try:
            query = """
            UPDATE usuario 
            SET username = ?, senha = ?, idade = ?, email = ?
            WHERE id_usuario = ?
            """
            params = (usuario.username, usuario.senha, usuario.idade, 
                      usuario.email, usuario.id_usuario)
            self._executar_query(query, params)
            return True
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar usuário: {str(e)}")

    def excluir(self, id_usuario):
        try:
            query = "DELETE FROM usuario WHERE id_usuario = ?"
            self._executar_query(query, (id_usuario,))
            return True
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir usuário: {str(e)}")

    def autenticar(self, username, senha):
        try:
            resultado = self.listar_por_username(username)
            if not resultado:
                raise UsuarioException.CredenciaisInvalidas(
                    "Username ou senha inválidos"
                )
            
            # Ordem de colunas: id_usuario, username, senha, idade, email
            id_usuario, username_db, senha_db, idade, email = resultado
            
            if senha_db != senha:
                raise UsuarioException.CredenciaisInvalidas(
                    "Username ou senha inválidos"
                )
            
            return resultado
        except UsuarioException:
            raise
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao autenticar: {str(e)}")

