import sys
from datetime import datetime, timedelta
from database import Database
from models.usuario import Usuario, UsuarioDAO
from models.livro import Livro, LivroDAO
from models.exemplar import Exemplar, ExemplarDAO
from models.emprestimo import Emprestimo, EmprestimoDAO
from models.solicitacaoemprestimo import SolicitacaoEmprestimo, SolicitacaoEmprestimoDAO
from models.avaliacaousuario import AvaliacaoUsuario, AvaliacaoUsuarioDAO
from exceptions import *

class Views:
    def usuario_listar():
        pass
    def usuario_listar_id(id):
        pass
    def usuario_atualizar(id):
        pass
    def usuario_excluir(id):
        pass

    def livro_listar():
        pass
    def livro_listar_id(id):
        pass
    def livro_atualizar(id):
        pass
    def livro_excluir(id):
        pass

    def exemplar_listar():
        pass
    def exemplar_listar_id(id):
        pass
    def exemplar_atualizar(id):
        pass
    def exemplar_excluir(id):
        pass
    
    def emprestimo_listar():
        pass
    def emprestimo_listar_id(id):
        pass
    def emprestimo_atualizar(id):
        pass
    def emprestimo_excluir(id):
        pass

    def solicitacao_listar():
        pass
    def solicitacao_listar_id(id):
        pass
    def solicitacao_atualizar(id):
        pass
    def solicitacao_excluir(id):
        pass

    def avaliacao_listar():
        pass
    def avaliacao_listar_id(id):
        pass
    def avaliacao_atualizar(id):
        pass
    def avaliacao_excluir(id):
        pass