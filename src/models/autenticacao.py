from DAO.usuarioDAO import UsuarioDAO
from exceptions import UsuarioException


class SistemaAutenticacao:
    
    def __init__(self, usuario_dao):
        self.usuario_dao = usuario_dao
        self.usuario_logado = None
        self.id_usuario_logado = None
    
    def fazer_login(self, username, senha):
        try:
            # Busca usuário no banco de dados
            resultado = self.usuario_dao.listar_por_username(username)
            
            if not resultado:
                raise UsuarioException.CredenciaisInvalidas(
                    "Username ou senha inválidos"
                )
            
            # Ordem: id_usuario, username, senha, idade, email
            id_usuario, username_db, senha_db, idade, email = resultado
            
            # Verifica senha (nota: em produção usar hash)
            if senha_db != senha:
                raise UsuarioException.CredenciaisInvalidas(
                    "Username ou senha inválidos"
                )
            
            # Estabelece sessão
            self.usuario_logado = {
                "id": id_usuario,
                "username": username_db,
                "email": email,
                "idade": idade
            }
            self.id_usuario_logado = id_usuario
            
            return True
            
        except UsuarioException:
            raise
        except Exception as e:
            raise UsuarioException.UsuarioNaoEncontrado(
                f"Erro ao realizar login: {str(e)}"
            )
    
    def fazer_logout(self):
        self.usuario_logado = None
        self.id_usuario_logado = None
    
    def esta_logado(self):
        return self.usuario_logado is not None
    
    def obter_usuario_logado(self):
        return self.usuario_logado
    
    def obter_id_usuario_logado(self):
        return self.id_usuario_logado
    
    def registrar_novo_usuario(self, username, email, idade, senha):
        try:
            if self.usuario_dao.listar_por_username(username):
                raise UsuarioException.UsuarioDuplicado(
                    "Username já registrado"
                )
            
            if self.usuario_dao.listar_por_email(email):
                raise UsuarioException.UsuarioDuplicado(
                    "Email já registrado"
                )
            
            from models.usuario import Usuario
            novo_usuario = Usuario(
                id_usuario=None,
                username=username,
                email=email,
                idade=idade,
                senha=senha
            )
            
            id_novo = self.usuario_dao.inserir(novo_usuario)
            
            return id_novo is not None
            
        except UsuarioException:
            raise
        except Exception as e:
            raise UsuarioException.DadosInvalidos(
                f"Erro ao registrar usuário: {str(e)}"
            )
    
    def alterar_senha(self, username, senha_antiga, senha_nova):
        try:
            resultado = self.usuario_dao.listar_por_username(username)
            
            if not resultado:
                raise UsuarioException.UsuarioNaoEncontrado(
                    "Usuário não encontrado"
                )
            
            id_usuario, username_db, senha_db, idade, email = resultado
            
            if senha_db != senha_antiga:
                raise UsuarioException.CredenciaisInvalidas(
                    "Senha atual inválida"
                )
            
            from models.usuario import Usuario
            usuario = Usuario(
                id_usuario=id_usuario,
                username=username_db,
                email=email,
                idade=idade,
                senha=senha_nova
            )
            
            return self.usuario_dao.atualizar(usuario)
            
        except UsuarioException:
            raise
        except Exception as e:
            raise UsuarioException.DadosInvalidos(
                f"Erro ao alterar senha: {str(e)}"
            )
