"""
DAO para Usuários - Implementa herança de BaseDAO
"""
from .dao import BaseDAO
from models.usuario import Usuario
from exceptions import UsuarioException, DAOException


class UsuarioDAO(BaseDAO):
    """
    DAO para gerenciar usuários.
    Herda de BaseDAO e implementa operações CRUD específicas para usuários.
    """

    def inserir(self, usuario):
        """
        Insere um novo usuário no banco de dados
        
        Args:
            usuario: Objeto Usuario a inserir
            
        Returns:
            ID do usuário inserido
            
        Raises:
            UsuarioException.DadosInvalidos: Se dados inválidos
            DAOException.OperacaoFalhou: Se operação falhar
        """
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
        """
        Lista todos os usuários
        
        Returns:
            Lista de tuplas com dados dos usuários
        """
        try:
            query = "SELECT * FROM usuario"
            return self._executar_query(query, fetch=True) or []
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar usuários: {str(e)}")

    def listar_por_id(self, id_usuario):
        """
        Lista um usuário por ID
        
        Args:
            id_usuario: ID do usuário
            
        Returns:
            Tupla com dados do usuário ou None
            
        Raises:
            UsuarioException.UsuarioNaoEncontrado: Se não encontrado
        """
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
        """
        Lista um usuário por email
        
        Args:
            email: Email do usuário
            
        Returns:
            Tupla com dados do usuário ou None
        """
        try:
            query = "SELECT * FROM usuario WHERE email = ?"
            return self._executar_query(query, (email,), fetch_one=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(
                f"Erro ao buscar usuário por email: {str(e)}"
            )

    def listar_por_username(self, username):
        """
        Lista um usuário por username
        
        Args:
            username: Username do usuário
            
        Returns:
            Tupla com dados do usuário ou None
        """
        try:
            query = "SELECT * FROM usuario WHERE username = ?"
            return self._executar_query(query, (username,), fetch_one=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(
                f"Erro ao buscar usuário por username: {str(e)}"
            )

    def atualizar(self, usuario):
        """
        Atualiza um usuário existente
        
        Args:
            usuario: Objeto Usuario com dados atualizados
            
        Returns:
            True se atualizado, False caso contrário
        """
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
        """
        Exclui um usuário
        
        Args:
            id_usuario: ID do usuário a excluir
            
        Returns:
            True se excluído, False caso contrário
        """
        try:
            query = "DELETE FROM usuario WHERE id_usuario = ?"
            self._executar_query(query, (id_usuario,))
            return True
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir usuário: {str(e)}")

    def autenticar(self, username, senha):
        """
        Autentica um usuário
        
        Args:
            username: Username do usuário
            senha: Senha do usuário
            
        Returns:
            Tupla com dados do usuário se credenciais válidas
            
        Raises:
            UsuarioException.CredenciaisInvalidas: Se credenciais inválidas
        """
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

