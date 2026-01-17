from exceptions import EmprestimoException, DAOException
from .dao import BaseDAO
from datetime import datetime, timedelta


class Emprestimo:
    
    DURACAO_DIAS = 14
    
    def __init__(self, id_emprestimo, id_solicitacao,
                 data_inicio, data_prevista, data_devolucao=None):
        self._id_emprestimo = id_emprestimo
        self._id_solicitacao = id_solicitacao
        self._data_inicio = None
        self._data_prevista = None
        self._data_devolucao = None
        
        self.set_data_inicio(data_inicio)
        self.set_data_prevista(data_prevista)
        if data_devolucao:
            self.set_data_devolucao(data_devolucao)

    def get_id(self):
        return self._id_emprestimo
    
    def set_id(self, id_emprestimo):
        self._id_emprestimo = id_emprestimo

    def get_id_solicitacao(self):
        return self._id_solicitacao
    
    def set_id_solicitacao(self, value):
        self._id_solicitacao = value

    def get_data_inicio(self):
        return self._data_inicio
    
    def set_data_inicio(self, value):
        self._validar_data(value)
        self._data_inicio = value

    def get_data_prevista(self):
        return self._data_prevista
    
    def set_data_prevista(self, value):
        self._validar_data(value)
        self._data_prevista = value

    def get_data_devolucao(self):
        return self._data_devolucao
    
    def set_data_devolucao(self, value):
        if value is not None:
            self._validar_data(value)
        self._data_devolucao = value

    def _validar_data(self, data):
        if isinstance(data, str):
            try:
                datetime.fromisoformat(data)
            except ValueError:
                raise EmprestimoException.DadosInvalidos(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )

    def esta_ativo(self):
        return self.get_data_devolucao() is None

    def esta_atrasado(self):
        if not self.esta_ativo():
            return False
        
        data_prevista = datetime.fromisoformat(self.get_data_prevista())
        return datetime.now() > data_prevista

    def dias_restantes(self):
        if not self.esta_ativo():
            return 0
        
        data_prevista = datetime.fromisoformat(self.get_data_prevista())
        dias = (data_prevista - datetime.now()).days
        return max(0, dias)

    def registrar_devolucao(self, data_devolucao=None):
        if not self.esta_ativo():
            raise EmprestimoException.EmprestimoInvalido(
                "Empréstimo já foi devolvido"
            )
        
        if data_devolucao is None:
            data_devolucao = datetime.now().strftime("%Y-%m-%d")
        
        self.set_data_devolucao(data_devolucao)

    def __str__(self):
        status = "Devolvido" if self.get_data_devolucao() else "Ativo"
        return f"Empréstimo({self.get_id_exemplar()}) - {status} - Prazo: {self.get_data_prevista()}"

    def __repr__(self):
        return f"Emprestimo(id={self.get_id()}, exemplar={self.get_id_exemplar()})"

    def __eq__(self, other):
        if not isinstance(other, Emprestimo):
            return False
        return self.get_id() == other.get_id()


class EmprestimoDAO(BaseDAO):

    def inserir(self, emprestimo):
        try:
            query = """
            INSERT INTO emprestimo 
            (id_exemplar, id_dono, id_emprestado, data_inicio, data_prevista, data_devolucao)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (emprestimo.get_id_exemplar(), emprestimo.get_id_dono(), 
                     emprestimo.get_id_emprestado(), emprestimo.get_data_inicio(), 
                     emprestimo.get_data_prevista(), emprestimo.get_data_devolucao())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir empréstimo: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM emprestimo"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar empréstimos: {str(e)}")

    def listar_id(self, id_emprestimo):
        try:
            query = "SELECT * FROM emprestimo WHERE id_emprestimo = ?"
            resultado = self._executar_query(query, (id_emprestimo,), fetch_one=True)
            if not resultado:
                raise EmprestimoException.EmprestimoNaoEncontrado(f"Empréstimo {id_emprestimo} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar empréstimo: {str(e)}")

    def atualizar(self, emprestimo):
        try:
            query = """
            UPDATE emprestimo 
            SET id_exemplar = ?, id_dono = ?, id_emprestado = ?, 
                data_inicio = ?, data_prevista = ?, data_devolucao = ?
            WHERE id_emprestimo = ?
            """
            params = (emprestimo.get_id_exemplar(), emprestimo.get_id_dono(), 
                     emprestimo.get_id_emprestado(), emprestimo.get_data_inicio(), 
                     emprestimo.get_data_prevista(), emprestimo.get_data_devolucao(), 
                     emprestimo.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar empréstimo: {str(e)}")

    def excluir(self, id_emprestimo):
        try:
            query = "DELETE FROM emprestimo WHERE id_emprestimo = ?"
            return self._executar_query(query, (id_emprestimo,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir empréstimo: {str(e)}")