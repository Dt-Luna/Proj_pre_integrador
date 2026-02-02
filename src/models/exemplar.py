from exceptions import ExemplarException, DAOException
from .dao import BaseDAO


class Exemplar:
    
    STATUS_DISPONIVEL = "disponivel"
    STATUS_EMPRESTADO = "emprestado"
    # STATUS_RESERVADO = "reservado"
    STATUSES_VALIDOS = [STATUS_DISPONIVEL, STATUS_EMPRESTADO]  # , STATUS_RESERVADO]
    
    def __init__(self, id_exemplar, id_usuario, id_livro, status):
        self._id_exemplar = id_exemplar
        self._id_usuario = id_usuario
        self._id_livro = id_livro
        self.set_status(status)

    def get_id(self):
        return self._id_exemplar
    
    def set_id(self, id_exemplar):
        self._id_exemplar = id_exemplar

    def get_id_usuario(self):
        return self._id_usuario
    
    def set_id_usuario(self, value):
        self._id_usuario = value

    def get_id_livro(self):
        return self._id_livro
    
    def set_id_livro(self, value):
        self._id_livro = value

    def get_status(self):
        return self._status
    
    def set_status(self, value):
        if value not in self.STATUSES_VALIDOS:
            raise ExemplarException.DadosInvalidos(
                f"Status '{value}' inválido. Use: {', '.join(self.STATUSES_VALIDOS)}"
            )
        self._status = value

    def esta_disponivel(self):
        return self.get_status() == self.STATUS_DISPONIVEL

    def emprestar(self):
        if not self.esta_disponivel():
            raise ExemplarException.ExemplarIndisponivel(
                f"Exemplar não está disponível (status: {self.get_status()})"
            )
        self.set_status(self.STATUS_EMPRESTADO)

    def devolver(self):
        self.set_status(self.STATUS_DISPONIVEL)

    # def reservar(self):
    #     if self.get_status() == self.STATUS_EMPRESTADO:
    #         self.set_status(self.STATUS_RESERVADO)
    #     elif not self.esta_disponivel():
    #         raise ExemplarException.ExemplarIndisponivel(
    #             f"Não é possível reservar exemplar com status: {self.get_status()}"
    #         )

    def __str__(self):
        return f"Exemplar({self.get_id()}) - Livro:{self.get_id_livro()} - {self.get_status()}"

    def __repr__(self):
        return f"Exemplar(id={self.get_id()}, livro={self.get_id_livro()})"


class ExemplarDAO(BaseDAO):

    def inserir(self, exemplar):
        try:
            query = """
            INSERT INTO exemplar 
            (id_usuario, id_livro, status)
            VALUES (?, ?, ?)
            """
            params = (exemplar.get_id_usuario(), exemplar.get_id_livro(), exemplar.get_status())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao inserir exemplar: {str(e)}")

    def listar(self):
        try:
            query = "SELECT * FROM exemplar"
            return self._executar_query(query, fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao listar exemplares: {str(e)}")

    def listar_id(self, id_exemplar):
        try:
            query = "SELECT * FROM exemplar WHERE id_exemplar = ?"
            resultado = self._executar_query(query, (id_exemplar,), fetch_one=True)
            if not resultado:
                raise ExemplarException.ExemplarNaoEncontrado(f"Exemplar {id_exemplar} não encontrado")
            return resultado
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplar: {str(e)}")

    def listar_por_usuario(self, id_usuario):
        # try:
            query = "SELECT * FROM exemplar WHERE id_usuario = ?"
            return self._executar_query(query, (id_usuario,), fetch=True)
        # except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplares do usuário: {str(e)}")

    def listar_por_livro(self, id_livro):
        try:
            query = "SELECT * FROM exemplar WHERE id_livro = ?"
            return self._executar_query(query, (id_livro,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplares do livro: {str(e)}")

    def listar_por_status(self, status):
        try:
            query = "SELECT * FROM exemplar WHERE status = ?"
            return self._executar_query(query, (status,), fetch=True)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao buscar exemplares por status: {str(e)}")

    def atualizar(self, exemplar):
        try:
            query = """
            UPDATE exemplar 
            SET id_usuario = ?, id_livro = ?, status = ?
            WHERE id_exemplar = ?
            """
            params = (exemplar.get_id_usuario(), exemplar.get_id_livro(), 
                     exemplar.get_status(), exemplar.get_id())
            return self._executar_query(query, params)
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao atualizar exemplar: {str(e)}")

    def excluir(self, id_exemplar):
        try:
            query = "DELETE FROM exemplar WHERE id_exemplar = ?"
            return self._executar_query(query, (id_exemplar,))
        except Exception as e:
            raise DAOException.OperacaoFalhou(f"Erro ao excluir exemplar: {str(e)}")