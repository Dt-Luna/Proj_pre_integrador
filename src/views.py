import sys
from datetime import datetime, timedelta
from dao.database import Database
from models.usuario import Usuario, UsuarioDAO
from models.livro import Livro, LivroDAO
from models.exemplar import Exemplar, ExemplarDAO
from models.emprestimo import Emprestimo, EmprestimoDAO
from models.solicitacaoemprestimo import SolicitacaoEmprestimo, SolicitacaoEmprestimoDAO
from models.avaliacaousuario import AvaliacaoUsuario, AvaliacaoUsuarioDAO
from exceptions import *

class Views:
    @staticmethod
    def usuario_autenticar(email, senha):
        # O DAO retorna uma TUPLA: (id, username, senha, nascimento, email)
        usuario = UsuarioDAO.autenticar(email, senha)
        
        if usuario:
            # Convertendo a Tupla para Dicionário
            return {
                "id": usuario[0],       # Índice 0 é o ID
                "username": usuario[1], # Índice 1 é o Username
                "senha": usuario[2],    # Índice 2 é a Senha
                "data_nascimento": usuario[3], # Índice 3 é a Data de Nascimento
                "email": usuario[4],    # Índice 4 é o Email
            }
        return None

    def criar_admin():
        UsuarioDAO.criar_admin_padrao()

    def usuario_inserir(nome, senha, email, data_nascimento):
        try:
            db = Database()
            dao = UsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        usuario = Usuario(None, nome, senha, email, data_nascimento)
        dao.inserir(usuario)

    def usuario_listar():
        try:
            db = Database()
            dao = UsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        return dao.listar()

    def usuario_listar_por_id(id):
        usuario = UsuarioDAO.listar_id(id)
        return usuario

    def usuario_listar_por_email(email):
        usuario = UsuarioDAO.listar_por_email(email)
        return usuario

    def usuario_listar_por_username(username):
        usuario = UsuarioDAO.listar_por_username(username)
        return usuario

    def usuario_atualizar(id, nome, senha, email, data_nascimento):
        usuario = Usuario(id, nome, senha, email, data_nascimento)
        # fazer conexao com o db e instanciar o dao (se repete nos outros metodos)
        try:
            db = Database()
            dao = UsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.atualizar(usuario)
 

    def usuario_excluir(id):
        db = Database()
        dao = UsuarioDAO(database=db.conn)
        dao.excluir(id)
###-------------------------------------------------------------------------------------###
    def livro_inserir(titulo, autor, paginas, isbn):
        try:
            db = Database()
            dao = LivroDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        livro = Livro(None, titulo, autor, paginas, isbn)
        dao.inserir(livro)

    def livro_listar():
        try:
            db = Database()
            dao = LivroDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        return dao.listar()

    def livro_listar_por_id(id):
        try:
            db = Database()
            dao = LivroDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        livro = dao.listar_id(id)
        return livro

    def livro_listar_por_titulo(titulo):
        try:
            db = Database()
            dao = LivroDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        livro = dao.listar_por_titulo(titulo)
        return livro

    def livro_atualizar(id, titulo, autor, paginas, isbn, capa):
        try:
            db = Database()
            dao = LivroDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        livro = Livro(id, titulo, autor, paginas, isbn, capa)
        dao.atualizar(livro)

    def livro_excluir(id):
        try:
            db = Database()
            dao = LivroDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.excluir(id)
###-------------------------------------------------------------------------------------###
    def exemplar_inserir(id_usuario, id_livro):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        exemplar = Exemplar(None, id_usuario, id_livro)
        dao.inserir(exemplar)

    def exemplar_listar():
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        return dao.listar()

    def exemplar_listar_por_id(id):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        exemplar = dao.listar_id(id)
        return exemplar

    def exemplar_listar_por_usuario(id_usuario):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        exemplar = dao.listar_por_usuario(id_usuario)
        return exemplar

    def exemplar_listar_por_livro(id_livro):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        exemplares = dao.listar_por_livro(id_livro)
        return exemplares

    def exemplar_listar_por_status(status):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        exemplar = dao.listar_por_status(status)
        return exemplar

    def exemplar_atualizar(id, id_usuario, id_livro, status):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        exemplar = Exemplar(id, id_usuario, id_livro, status)
        dao.atualizar(exemplar)

    def exemplar_excluir(id):
        try:
            db = Database()
            dao = ExemplarDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.excluir(id)
###-------------------------------------------------------------------------------------###
    def emprestimo_inserir(id_solicitacao, data_inicio, data_prevista):
        emprestimo = Emprestimo(None, id_solicitacao, data_inicio, data_prevista)
        EmprestimoDAO.inserir(emprestimo)
        
    def emprestimo_listar():
        r = EmprestimoDAO.listar()
        return r
    
    def emprestimo_listar_id(id):
        emprestimo = EmprestimoDAO.listar_id(id)
        return emprestimo
    def emprestimo_atualizar(id, id_solicitacao, data_inicio, data_prevista, data_devolucao):
        emprestimo = Emprestimo(id, id_solicitacao, data_inicio, data_prevista)
        emprestimo.set_data_devolucao(data_devolucao)
        EmprestimoDAO.atualizar(emprestimo)
        
    def emprestimo_excluir(id):
        EmprestimoDAO.excluir(id)
###-------------------------------------------------------------------------------------###
    def solicitacao_inserir(id_usuario, id_livro, dias_emprestimo):
        solicitacao = SolicitacaoEmprestimo(None, datetime.now().strftime("%Y-%m-%d"), "pendente", dias_emprestimo, id_livro, id_usuario)
        SolicitacaoEmprestimoDAO.inserir(solicitacao)
        
    def solicitacao_listar():
        r = SolicitacaoEmprestimoDAO.listar()
        return r

    def solicitacao_listar_id(id):
        return SolicitacaoEmprestimoDAO.listar_id(id)
    def solicitacao_atualizar(id, status, dias_emprestimo, id_exemplar, id_solicitante):
        solicitacao = SolicitacaoEmprestimo(id, datetime.now().strftime("%Y-%m-%d"), status, dias_emprestimo, id_exemplar, id_solicitante)
        SolicitacaoEmprestimoDAO.atualizar(solicitacao)
    def solicitacao_excluir(id):
        SolicitacaoEmprestimoDAO.excluir(id)
###-------------------------------------------------------------------------------------###
    def avaliacao_inserir(id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo):
        avaliacao = AvaliacaoUsuario(None, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo)
        try:
            db = Database()
            dao = AvaliacaoUsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.inserir(avaliacao)
        #
        AvaliacaoUsuarioDAO.inserir(avaliacao)

    def avaliacao_listar():
        try:
            db = Database()
            dao = AvaliacaoUsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        return dao.listar()

    def avaliacao_listar_id(id):
        return AvaliacaoUsuarioDAO.listar_id(id)
    def avaliacao_atualizar(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo):
        avaliacao = AvaliacaoUsuario(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo)
        try:
            db = Database()
            dao = AvaliacaoUsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.atualizar(avaliacao)
        #
    def avaliacao_excluir(id):
        try:
            db = Database()
            dao = AvaliacaoUsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.excluir(id)