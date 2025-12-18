from exceptions import EmprestimoException
from datetime import datetime, timedelta


class Emprestimo:
    
    DURACAO_DIAS = 14  
    
    def __init__(self, id_emprestimo, id_exemplar, id_dono, id_emprestado,
                 data_inicio, data_prevista, data_devolucao=None):
        self._id_emprestimo = id_emprestimo
        self._id_exemplar = id_exemplar
        self._id_dono = id_dono
        self._id_emprestado = id_emprestado
        self.data_inicio = data_inicio  
        self.data_prevista = data_prevista  
        self.data_devolucao = data_devolucao

    @property
    def id_emprestimo(self):
        return self._id_emprestimo

    @property
    def id_exemplar(self):
        return self._id_exemplar

    @property
    def id_dono(self):
        return self._id_dono

    @property
    def id_emprestado(self):
        return self._id_emprestado

    @property
    def data_inicio(self):
        return self._data_inicio
    
    @data_inicio.setter
    def data_inicio(self, value):
        self._validar_data(value)
        self._data_inicio = value

    @property
    def data_prevista(self):
        return self._data_prevista
    
    @data_prevista.setter
    def data_prevista(self, value):
        self._validar_data(value)
        self._data_prevista = value

    @property
    def data_devolucao(self):
        return self._data_devolucao
    
    @data_devolucao.setter
    def data_devolucao(self, value):
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
        return self.data_devolucao is None

    def esta_atrasado(self):
        if not self.esta_ativo():
            return False
        
        data_prevista = datetime.fromisoformat(self.data_prevista)
        return datetime.now() > data_prevista

    def dias_restantes(self):
        if not self.esta_ativo():
            return 0
        
        data_prevista = datetime.fromisoformat(self.data_prevista)
        dias = (data_prevista - datetime.now()).days
        return max(0, dias)

    def registrar_devolucao(self, data_devolucao=None):
        if not self.esta_ativo():
            raise EmprestimoException.EmprestimoInvalido(
                "Empréstimo já foi devolvido"
            )
        
        if data_devolucao is None:
            data_devolucao = datetime.now().strftime("%Y-%m-%d")
        
        self.data_devolucao = data_devolucao

    def __str__(self):
        status = "Devolvido" if self.data_devolucao else "Ativo"
        return f"Empréstimo({self.id_exemplar}) - {status} - Prazo: {self.data_prevista}"

    def __repr__(self):
        """Representação técnica do empréstimo"""
        return f"Emprestimo(id={self.id_emprestimo}, exemplar={self.id_exemplar})"

    def __eq__(self, other):
        """Compara empréstimos por ID"""
        if not isinstance(other, Emprestimo):
            return False
        return self.id_emprestimo == other.id_emprestimo
