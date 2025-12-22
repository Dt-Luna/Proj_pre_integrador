from exceptions import UsuarioException, DAOException
from .dao import BaseDAO


class Usuario:
    
    def __init__(self, id_usuario, username, senha, email, idade):
        self._id_usuario = id_usuario
        self._username = None
        self._senha = None
        self._email = None
        self._idade = None
        
        self.set_username(username)
        self.set_senha(senha)
        self.set_email(email)
        self.set_idade(idade)

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

    def get_idade(self):
        return self._idade
    
    def set_idade(self, value):
        if value < 18 or value > 120:
            raise UsuarioException.DadosInvalidos(
                "Idade deve estar entre 18 e 120 anos"
            )
        self._idade = int(value)

    def __str__(self):
        return f"{self.get_username()} - {self.get_idade()} anos ({self.get_email()})"

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
            (username, senha, idade, email)
            VALUES (?, ?, ?, ?)
            """
            params = (usuario.get_username(), usuario.get_senha(), 
                     usuario.get_idade(), usuario.get_email())
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
            SET username = ?, senha = ?, email = ?, idade = ?
            WHERE id_usuario = ?
            """
            params = (usuario.get_username(), usuario.get_senha(), 
                     usuario.get_email(), usuario.get_idade(), usuario.get_id())
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