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
    def usuario_autenticar(email, senha):
        usuario = UsuarioDAO.autenticar(email, senha)
        if usuario:
            return {
                "id": usuario.get_id(),
                "username": usuario.get_username(),
                "email": usuario.get_email(),
            }
        return None

    def criar_admin():
        UsuarioDAO.criar_admin_padrao()

    def usuario_inserir(nome, senha, email, data_nascimento):
        usuario = Usuario(None, nome, senha, email, data_nascimento)
        UsuarioDAO.inserir(usuario)

    def usuario_listar():
        r = UsuarioDAO.listar()
        return r

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
        UsuarioDAO.atualizar(usuario)

    def usuario_excluir(id):
        UsuarioDAO.excluir(id)
###-------------------------------------------------------------------------------------###
    def livro_inserir(titulo, autor, paginas, isbn):
        livro = Livro(None, titulo, autor, paginas, isbn)
        LivroDAO.inserir(livro)

    def livro_listar():
        r = LivroDAO.listar()
        return r

    def livro_listar_por_id(id):
        livro = LivroDAO.listar_id(id)
        return livro

    def livro_listar_por_titulo(titulo):
        livro = LivroDAO.listar_por_titulo(titulo)
        return livro

    def livro_atualizar(id, titulo, autor, paginas, isbn, capa):
        livro = Livro(id, titulo, autor, paginas, isbn)
        livro.set_capa(capa)
        LivroDAO.atualizar(livro)

    def livro_excluir(id):
        LivroDAO.excluir(id)
###-------------------------------------------------------------------------------------###
    def exemplar_inserir(id_usuario, id_livro):
        exemplar = Exemplar(None, id_usuario, id_livro)
        ExemplarDAO.inserir(exemplar)

    def exemplar_listar():
        r = ExemplarDAO.listar()
        return r

    def exemplar_listar_por_id(id):
        exemplar = ExemplarDAO.listar_id(id)
        return exemplar

    def exemplar_listar_por_usuario(id_usuario):
        exemplar = ExemplarDAO.listar_por_usuario(id_usuario)
        return exemplar

    def exemplar_listar_por_livro(id_livro):
        exemplar = ExemplarDAO.listar_por_livro(id_livro)
        return exemplar

    def exemplar_listar_por_status(status):
        exemplar = ExemplarDAO.listar_por_status(status)
        return exemplar

    def exemplar_atualizar(id, id_usuario, id_livro, status):
        exemplar = Exemplar(id, id_usuario, id_livro)
        exemplar.set_status(status)
        ExemplarDAO.atualizar(exemplar)

    def exemplar_excluir(id):
        ExemplarDAO.excluir(id)
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
        AvaliacaoUsuarioDAO.inserir(avaliacao)
    def avaliacao_listar():
        r = AvaliacaoUsuarioDAO.listar()
        return r
    def avaliacao_listar_id(id):
        return AvaliacaoUsuarioDAO.listar_id(id)
    def avaliacao_atualizar(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo):
        avaliacao = AvaliacaoUsuario(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo)
        AvaliacaoUsuarioDAO.atualizar(avaliacao)
    def avaliacao_excluir(id):
        AvaliacaoUsuarioDAO.excluir(id)