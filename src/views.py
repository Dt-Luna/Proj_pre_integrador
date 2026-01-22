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
                "email": usuario[4],    # Índice 4 é o Email
                "data_nascimento": usuario[3],  # Índice 3 é a data de nascimento
            }
        return None

    @staticmethod
    def criar_admin():
        from models.dao import BaseDAO
        BaseDAO.criar_admin_padrao()

    def usuario_inserir(nome, senha, email, data_nascimento):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            usuario = Usuario(None, nome, senha, email, data_nascimento)
            dao = UsuarioDAO(conn)
            dao.inserir(usuario)
        finally:
            conn.close()

    def usuario_listar():
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = UsuarioDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()

    def usuario_listar_por_id(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = UsuarioDAO(conn)
            usuario = dao.listar_id(id)
            return usuario
        finally:
            conn.close()

    def usuario_listar_por_email(email):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = UsuarioDAO(conn)
            usuario = dao.listar_por_email(email)
            return usuario
        finally:
            conn.close()

    def usuario_listar_por_username(username):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = UsuarioDAO(conn)
            usuario = dao.listar_por_username(username)
            return usuario
        finally:
            conn.close()

    def usuario_atualizar(id, nome, senha, email, data_nascimento):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            usuario = Usuario(id, nome, senha, email, data_nascimento)
            dao = UsuarioDAO(conn)
            dao.atualizar(usuario)
        finally:
            conn.close()

    def usuario_excluir(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = UsuarioDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()
###-------------------------------------------------------------------------------------###
    def livro_inserir(titulo, autor, paginas, isbn):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            livro = Livro(None, titulo, autor, paginas, isbn)
            dao = LivroDAO(conn)
            dao.inserir(livro)
        finally:
            conn.close()

    def livro_listar():
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = LivroDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()

    def livro_listar_por_id(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = LivroDAO(conn)
            livro = dao.listar_id(id)
            return livro
        finally:
            conn.close()

    def livro_listar_por_titulo(titulo):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = LivroDAO(conn)
            livro = dao.listar_por_titulo(titulo)
            return livro
        finally:
            conn.close()

    def livro_atualizar(id, titulo, autor, paginas, isbn, capa):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            livro = Livro(id, titulo, autor, paginas, isbn)
            livro.set_capa(capa)
            dao = LivroDAO(conn)
            dao.atualizar(livro)
        finally:
            conn.close()

    def livro_excluir(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = LivroDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()
###-------------------------------------------------------------------------------------###
    def exemplar_inserir(id_usuario, id_livro):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            exemplar = Exemplar(None, id_usuario, id_livro)
            dao = ExemplarDAO(conn)
            dao.inserir(exemplar)
        finally:
            conn.close()

    def exemplar_listar():
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = ExemplarDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()

    def exemplar_listar_por_id(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = ExemplarDAO(conn)
            exemplar = dao.listar_id(id)
            return exemplar
        finally:
            conn.close()

    def exemplar_listar_por_usuario(id_usuario):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = ExemplarDAO(conn)
            exemplar = dao.listar_por_usuario(id_usuario)
            return exemplar
        finally:
            conn.close()

    def exemplar_listar_por_livro(id_livro):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = ExemplarDAO(conn)
            exemplar = dao.listar_por_livro(id_livro)
            return exemplar
        finally:
            conn.close()

    def exemplar_listar_por_status(status):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = ExemplarDAO(conn)
            exemplar = dao.listar_por_status(status)
            return exemplar
        finally:
            conn.close()

    def exemplar_atualizar(id, id_usuario, id_livro, status):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            exemplar = Exemplar(id, id_usuario, id_livro)
            exemplar.set_status(status)
            dao = ExemplarDAO(conn)
            dao.atualizar(exemplar)
        finally:
            conn.close()

    def exemplar_excluir(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = ExemplarDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()
###-------------------------------------------------------------------------------------###
    def emprestimo_inserir(id_solicitacao, data_inicio, data_prevista):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            emprestimo = Emprestimo(None, id_solicitacao, data_inicio, data_prevista)
            dao = EmprestimoDAO(conn)
            dao.inserir(emprestimo)
        finally:
            conn.close()
        
    def emprestimo_listar():
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = EmprestimoDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()
    
    def emprestimo_listar_id(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = EmprestimoDAO(conn)
            emprestimo = dao.listar_id(id)
            return emprestimo
        finally:
            conn.close()

    def emprestimo_atualizar(id, id_solicitacao, data_inicio, data_prevista, data_devolucao):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            emprestimo = Emprestimo(id, id_solicitacao, data_inicio, data_prevista)
            emprestimo.set_data_devolucao(data_devolucao)
            dao = EmprestimoDAO(conn)
            dao.atualizar(emprestimo)
        finally:
            conn.close()
        
    def emprestimo_excluir(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = EmprestimoDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()
###-------------------------------------------------------------------------------------###
    def solicitacao_inserir(id_usuario, id_livro, dias_emprestimo):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            solicitacao = SolicitacaoEmprestimo(None, datetime.now().strftime("%Y-%m-%d"), "pendente", dias_emprestimo, id_livro, id_usuario)
            dao = SolicitacaoEmprestimoDAO(conn)
            dao.inserir(solicitacao)
        finally:
            conn.close()
        
    def solicitacao_listar():
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()

    def solicitacao_listar_id(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            return dao.listar_id(id)
        finally:
            conn.close()

    def solicitacao_atualizar(id, status, dias_emprestimo, id_exemplar, id_solicitante):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            solicitacao = SolicitacaoEmprestimo(id, datetime.now().strftime("%Y-%m-%d"), status, dias_emprestimo, id_exemplar, id_solicitante)
            dao = SolicitacaoEmprestimoDAO(conn)
            dao.atualizar(solicitacao)
        finally:
            conn.close()

    def solicitacao_excluir(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()
###-------------------------------------------------------------------------------------###
    def avaliacao_inserir(id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            avaliacao = AvaliacaoUsuario(None, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo)
            dao = AvaliacaoUsuarioDAO(conn)
            dao.inserir(avaliacao)
        finally:
            conn.close()

    def avaliacao_listar():
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = AvaliacaoUsuarioDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()

    def avaliacao_listar_id(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = AvaliacaoUsuarioDAO(conn)
            return dao.listar_id(id)
        finally:
            conn.close()

    def avaliacao_atualizar(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            avaliacao = AvaliacaoUsuario(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo)
            dao = AvaliacaoUsuarioDAO(conn)
            dao.atualizar(avaliacao)
        finally:
            conn.close()

    def avaliacao_excluir(id):
        import sqlite3
        conn = sqlite3.connect('bookshare.db')
        try:
            dao = AvaliacaoUsuarioDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()