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

import sqlite3
conn = sqlite3.connect('bookshare.db')

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
        else:
            raise ValueError("Email ou senha inválidos.")

    @staticmethod
    def criar_admin():
        from models.dao import BaseDAO
        BaseDAO.criar_admin_padrao()

    def usuario_inserir(nome, senha, email, data_nascimento):
        if not nome or not senha or not email or not data_nascimento:
            raise ValueError("Todos os campos são obrigatórios.")
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
    
        try:
            dao = UsuarioDAO(conn)
            usuario = dao.listar_id(id)
            return usuario
        finally:
            conn.close()

    def usuario_listar_por_email(email):
    
        try:
            dao = UsuarioDAO(conn)
            usuario = dao.listar_por_email(email)
            return usuario
        finally:
            conn.close()

    def usuario_listar_por_username(username):
    
        try:
            dao = UsuarioDAO(conn)
            usuario = dao.listar_por_username(username)
            return usuario
        finally:
            conn.close()

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
        exemplar = Exemplar(None, id_usuario, id_livro, 'disponivel')
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
        exemplares = dao.listar_por_usuario(id_usuario)
        return exemplares

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
    
        try:
            emprestimo = Emprestimo(None, id_solicitacao, data_inicio, data_prevista)
            dao = EmprestimoDAO(conn)
            dao.inserir(emprestimo)
        finally:
            conn.close()
        
    def emprestimo_listar():
    
        try:
            dao = EmprestimoDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()
    
    def emprestimo_listar_id(id):
    
        try:
            dao = EmprestimoDAO(conn)
            emprestimo = dao.listar_id(id)
            return emprestimo
        finally:
            conn.close()

    def emprestimo_atualizar(id, id_solicitacao, data_inicio, data_prevista, data_devolucao):
    
        try:
            emprestimo = Emprestimo(id, id_solicitacao, data_inicio, data_prevista)
            emprestimo.set_data_devolucao(data_devolucao)
            dao = EmprestimoDAO(conn)
            dao.atualizar(emprestimo)
        finally:
            conn.close()
        
    def emprestimo_excluir(id):

        try:
            dao = EmprestimoDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()

    def emprestimo_listar_por_usuario(id_usuario):

        try:
            dao = EmprestimoDAO(conn)
            return dao.listar_por_usuario(id_usuario)
        finally:
            conn.close()
###-------------------------------------------------------------------------------------###
    def solicitacao_inserir(id_usuario, id_exemplar, dias_emprestimo):
    
        try:
            solicitacao = SolicitacaoEmprestimo(None, datetime.now().strftime("%Y-%m-%d"), "pendente", dias_emprestimo, id_exemplar, id_usuario)
            dao = SolicitacaoEmprestimoDAO(conn)
            dao.inserir(solicitacao)
        finally:
            conn.close()
        
    def solicitacao_listar():
    
        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            r = dao.listar()
            return r
        finally:
            conn.close()

    def solicitacao_listar_id(id):
    
        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            return dao.listar_id(id)
        finally:
            conn.close()

    def solicitacao_atualizar(id, status, dias_emprestimo, id_exemplar, id_solicitante):

        try:
            # Get existing solicitacao to keep original data
            existing = Views.solicitacao_listar_id(id)
            solicitacao = SolicitacaoEmprestimo(id, existing[1], status, dias_emprestimo, id_exemplar, id_solicitante)
            dao = SolicitacaoEmprestimoDAO(conn)
            dao.atualizar(solicitacao)
        finally:
            conn.close()

    def solicitacao_excluir(id):

        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            dao.excluir(id)
        finally:
            conn.close()

    def solicitacao_listar_por_usuario(id_usuario):

        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            return dao.listar_por_usuario(id_usuario)
        finally:
            conn.close()

    def solicitacao_listar_por_exemplar(id_exemplar):

        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            return dao.listar_por_exemplar(id_exemplar)
        finally:
            conn.close()

    def solicitacao_listar_pendentes_por_dono(id_dono):

        try:
            dao = SolicitacaoEmprestimoDAO(conn)
            return dao.listar_pendentes_por_dono(id_dono)
        finally:
            conn.close()

    def aprovar_solicitacao(id_solicitacao):
        try:
            # Get solicitacao
            solicitacao = Views.solicitacao_listar_id(id_solicitacao)
            id_exemplar = solicitacao[4]
            dias_emprestimo = solicitacao[3]

            # Update solicitacao status
            Views.solicitacao_atualizar(id_solicitacao, 'aceita', dias_emprestimo, id_exemplar, solicitacao[5])

            # Create emprestimo
            data_inicio = datetime.now().strftime("%Y-%m-%d")
            data_prevista = (datetime.now() + timedelta(days=dias_emprestimo)).strftime("%Y-%m-%d")
            Views.emprestimo_inserir(id_solicitacao, data_inicio, data_prevista)

            # Update exemplar status
            exemplar = Views.exemplar_listar_por_id(id_exemplar)
            Views.exemplar_atualizar(id_exemplar, exemplar[1], exemplar[2], 'emprestado')

        except Exception as e:
            raise Exception(f"Erro ao aprovar solicitação: {str(e)}")

    def rejeitar_solicitacao(id_solicitacao):
        try:
            solicitacao = Views.solicitacao_listar_id(id_solicitacao)
            Views.solicitacao_atualizar(id_solicitacao, 'recusada', solicitacao[3], solicitacao[4], solicitacao[5])
        except Exception as e:
            raise Exception(f"Erro ao rejeitar solicitação: {str(e)}")

    def confirmar_devolucao(id_emprestimo):
        try:
            # Update emprestimo
            emprestimo = Views.emprestimo_listar_id(id_emprestimo)
            Views.emprestimo_atualizar(id_emprestimo, emprestimo[1], emprestimo[2], emprestimo[3], datetime.now().strftime("%Y-%m-%d"))

            # Get exemplar from solicitacao
            solicitacao = Views.solicitacao_listar_id(emprestimo[1])
            id_exemplar = solicitacao[4]
            exemplar = Views.exemplar_listar_por_id(id_exemplar)
            Views.exemplar_atualizar(id_exemplar, exemplar[1], exemplar[2], 'disponivel')

        except Exception as e:
            raise Exception(f"Erro ao confirmar devolução: {str(e)}")

    def solicitar_devolucao(id_emprestimo):
        try:
            emprestimo = Views.emprestimo_listar_id(id_emprestimo)
            if emprestimo[4] is not None:
                raise Exception("Empréstimo já foi devolvido")
            Views.emprestimo_atualizar(id_emprestimo, emprestimo[1], emprestimo[2], emprestimo[3], datetime.now().strftime("%Y-%m-%d"))
        except Exception as e:
            raise Exception(f"Erro ao solicitar devolução: {str(e)}")

    def listar_devolucoes_pendentes_por_dono(id_dono):
        try:
            dao = EmprestimoDAO(conn)
            # Query to get emprestimos where data_devolucao is set and exemplar is still emprestado and belongs to dono
            query = """
            SELECT e.* FROM emprestimo e
            JOIN solicitacao_emprestimo s ON e.id_solicitacao = s.id_solicitacao
            JOIN exemplar ex ON s.id_exemplar = ex.id_exemplar
            WHERE ex.id_usuario = ? AND e.data_devolucao IS NOT NULL AND ex.status = 'emprestado'
            """
            return dao._executar_query(query, (id_dono,), fetch=True)
        finally:
            conn.close()

###-------------------------------------------------------------------------------------###
    def avaliacao_inserir(id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo):
        avaliacao = AvaliacaoUsuario(None, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo)
        try:
            db = Database()
            dao = AvaliacaoUsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        dao.inserir(avaliacao)

    def avaliacao_listar():
        try:
            db = Database()
            dao = AvaliacaoUsuarioDAO(db.conn)
        except Exception as e:
            raise DAOException.ConexaoFalhou(f"Erro ao conectar ao banco de dados: {str(e)}")
        return dao.listar()

    def avaliacao_listar_id(id):
    
        try:
            dao = AvaliacaoUsuarioDAO(conn)
            return dao.listar_id(id)
        finally:
            conn.close()

    def avaliacao_listar_por_avaliador_emprestimo(id_avaliador, id_emprestimo):
        try:
            dao = AvaliacaoUsuarioDAO(conn)
            return dao.listar_por_avaliador_emprestimo(id_avaliador, id_emprestimo)
        finally:
            conn.close()
        

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