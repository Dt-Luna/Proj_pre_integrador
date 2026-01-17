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
        for c in Views.usuario_listar():
            if c.get_email() == email and c.get_senha() == senha: return{"id": c.get_id(), "nome": c.get_nome(), "email": c.get_email}
        return None

    def criar_admin():
        list = Views.usuario_listar()
        for c in list:
            if c.get_email() == "admin" and c.get_nome() == "admin": return
        Views.usuario_inserir("admin", "1234", "admin", 20)

    def usuario_inserir(nome, senha, email, idade):
        usuario = Usuario(nome, senha, email, idade)
        UsuarioDAO.inserir(usuario)

    def usuario_listar():
        r = UsuarioDAO.listar()
        r.sort(key = lambda obj : obj.get_nome())
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

    def usuario_atualizar(id, nome, senha, email, idade):
        usuario = Usuario(id, nome, senha, email, idade)
        UsuarioDAO.atualizar(usuario)

    def usuario_excluir(id):
        usuario = Usuario(id, "", "", "", "")
        UsuarioDAO.excluir(usuario)
###-------------------------------------------------------------------------------------###
    def livro_inserir(titulo, autor, paginas):
        livro = Livro(titulo, autor, paginas)
        LivroDAO.inserir(livro)

    def livro_listar():
        r = LivroDAO.listar()
        r.sort(key = lambda obj : obj.get_titulo())
        return r

    def livro_listar_por_id(id):
        livro = LivroDAO.listar_id(id)
        return livro

    def livro_listar_por_autor(autor):
        livro = LivroDAO.listar_por_autor(autor)
        return livro

    def livro_listar_por_titulo(titulo):
        livro = LivroDAO.listar_por_titulo(titulo)
        return livro

    def livro_atualizar(id, titulo, autor, paginas, capa):
        livro = Livro(id, titulo, autor, paginas)
        livro.set_capa(capa)
        LivroDAO.atualizar(livro)

    def livro_excluir(id):
        livro = Livro(id, "", "", "", "")
        LivroDAO.excluir(livro)
###-------------------------------------------------------------------------------------###
    def exemplar_inserir(id_usuario, id_livro):
        exemplar = Exemplar(id_usuario, id_livro)
        ExemplarDAO.inserir(exemplar)

    def exemplar_listar():
        r = ExemplarDAO.listar()
        r.sort(key = lambda obj : obj.get_nome())
        return r

    def exemplar_listar_por_id(id):
        exemplar = ExemplarDAO.listar_id()
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
        exemplar = Exemplar(id, "", "", "")
        ExemplarDAO.excluir(exemplar)
###-------------------------------------------------------------------------------------###
    def emprestimo_inserir():
        pass
    def emprestimo_listar():
        r = EmprestimoDAO.listar()
        r.sort(key = lambda obj : obj.get_nome())
        return r
    def emprestimo_listar_id(id):
        pass
    def emprestimo_atualizar(id):
        pass
    def emprestimo_excluir(id):
        pass
###-------------------------------------------------------------------------------------###
    def solicitacao_inserir():
        pass
    def solicitacao_listar():
        r = UsuarioDAO.listar()
        r.sort(key = lambda obj : obj.get_nome())
        return r
    def solicitacao_listar_id(id):
        pass
    def solicitacao_atualizar(id):
        pass
    def solicitacao_excluir(id):
        pass
###-------------------------------------------------------------------------------------###
    def avaliacao_inserir():
        pass
    def avaliacao_listar():
        r = UsuarioDAO.listar()
        r.sort(key = lambda obj : obj.get_nome())
        return r
    def avaliacao_listar_id(id):
        pass
    def avaliacao_atualizar(id):
        pass
    def avaliacao_excluir(id):
        pass