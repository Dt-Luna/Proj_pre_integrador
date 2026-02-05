from exceptions import UsuarioException, DAOException
from datetime import datetime
from .dao import BaseDAO
import sqlite3


class Usuario:
    
    def __init__(self, id_usuario, username, senha, email, data_nascimento):
        self._id_usuario = id_usuario
        if not email:
            raise ValueError("Email é obrigatório.")
        if not data_nascimento:
            raise ValueError("Data de nascimento é obrigatória.")
        self._username = None
        self._senha = None
        self._email = None
        self._data_nascimento = None
            
        self.set_username(username)
        self.set_senha(senha)
        self.set_email(email)
        self.set_data_nascimento(data_nascimento)

    def get_id(self):
        return self._id_usuario
    
    def set_id(self, id_usuario):
        self._id_usuario = id_usuario

    def get_username(self):
        return self._username
    
    def set_username(self, value):
        if not value or len(value.strip()) < 3:
            raise UsuarioException.DadosInvalidos(
                "Username deve ter pelo menos 3 caracteres"
            )
        self._username = value.strip()

    def get_senha(self):
        return self._senha
    
    def set_senha(self, value):
        if not value or len(value) < 6:
            raise UsuarioException.DadosInvalidos(
                "Senha deve ter pelo menos 6 caracteres"
            )
        self._senha = value

    def get_email(self):
        return self._email
    
    def set_email(self, value):
        if "@" not in value or "." not in value:
            raise UsuarioException.DadosInvalidos(
                "Email inválido"
            )
        self._email = value.lower()

    def set_data_nascimento(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self._data_nascimento = value
        except ValueError:
            raise UsuarioException.DadosInvalidos(
                "Data de nascimento deve estar no formato YYYY-MM-DD"
            )

    def get_data_nascimento(self):
        return self._data_nascimento

    def __str__(self):
        return f"{self.get_username()} - {(self.get_data_nascimento() - datetime.date.today()).year} ({self.get_email()})"
    def __repr__(self):
        return f"Usuario(id={self.get_id()}, username='{self.get_username()}')"

    def __eq__(self, other):
        if not isinstance(other, Usuario):
            return False
        return self.get_id() == other.get_id()


class UsuarioDAO(BaseDAO):

    def inserir(self, usuario):
        try:
            query = """
            INSERT INTO usuario 
            (username, senha, data_nascimento, email)
            VALUES (?, ?, ?, ?)
            """
            params = (usuario.get_username(), usuario.get_senha(), 
                     BaseDAO._converter_str_to_data(usuario.get_data_nascimento()), usuario.get_email())
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
            query = "SELECT * FROM usuario ORDER BY username ASC"
            return self._executar_query(query, fetch=True) or []
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar usuários: {str(e)}")

    def listar_seguro(self):
        try:
            query = "SELECT id_usuario, username, email, data_nascimento FROM usuario ORDER BY username ASC"
            return self._executar_query(query, fetch=True) or []
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar usuários: {str(e)}")

    def listar_id_seguro(self, id_usuario):
        """Busca usuário por ID sem incluir a senha nos resultados"""
        try:
            query = "SELECT id_usuario, username, email, data_nascimento FROM usuario WHERE id_usuario = ?"
            resultado = self._executar_query(query, (id_usuario,), fetch_one=True)
            if not resultado:
                raise UsuarioException.UsuarioNaoEncontrado(
                    f"Usuário {id_usuario} não encontrado"
                )
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar usuário: {str(e)}")

    def listar_id(self, id_usuario):
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
            SET username = ?, senha = ?, email = ?, data_nascimento = ?
            WHERE id_usuario = ?
            """
            params = (usuario.get_username(), usuario.get_senha(), 
                     usuario.get_email(), BaseDAO._converter_str_to_data(usuario.get_data_nascimento()), usuario.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar usuário: {str(e)}")

    def excluir(self, id_usuario):
        try:
            query = "DELETE FROM usuario WHERE id_usuario = ?"
            self._executar_query(query, (id_usuario,))
            return True
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir usuário: {str(e)}")

    @classmethod
    def autenticar(cls, email, senha):
        conn = None
        try:
            conn = sqlite3.connect('bookshare.db') # Verifique se o nome do banco está correto
            
            dao = cls(conn) 
            
            resultado = dao.listar_por_email(email.lower())
            
            if not resultado:
                raise UsuarioException.CredenciaisInvalidas("Email ou senha inválidos")
            
            id_usuario = resultado[0]
            username_db = resultado[1]
            senha_db = resultado[2]
            
            if senha_db != senha:
                raise UsuarioException.CredenciaisInvalidas("Email ou senha inválidos")
            
            return resultado
            
        except UsuarioException:
            raise
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao autenticar: {str(e)}")
        finally:
            if conn:
                conn.close()