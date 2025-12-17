"""
Modelo de Empréstimo - Implementa encapsulamento com propriedades
"""
from exceptions import EmprestimoException
from datetime import datetime, timedelta


class Emprestimo:
    """
    Modelo de empréstimo de livro do sistema.
    Implementa encapsulamento de atributos com validação.
    """
    
    DURACAO_DIAS = 14  # Empréstimo com duração padrão de 14 dias
    
    def __init__(self, id_emprestimo, id_exemplar, id_dono, id_emprestado,
                 data_inicio, data_prevista, data_devolucao=None):
        """
        Inicializa um novo empréstimo
        
        Args:
            id_emprestimo: ID único do empréstimo
            id_exemplar: ID do exemplar emprestado
            id_dono: ID do usuário dono do exemplar
            id_emprestado: ID do usuário que pegou emprestado
            data_inicio: Data de início do empréstimo
            data_prevista: Data prevista de devolução
            data_devolucao: Data real de devolução (None se não devolvido)
            
        Raises:
            EmprestimoException.DadosInvalidos: Se dados inválidos
        """
        self._id_emprestimo = id_emprestimo
        self._id_exemplar = id_exemplar
        self._id_dono = id_dono
        self._id_emprestado = id_emprestado
        self.data_inicio = data_inicio  # Usa property
        self.data_prevista = data_prevista  # Usa property
        self.data_devolucao = data_devolucao  # Usa property

    @property
    def id_emprestimo(self):
        """Getter do ID do empréstimo"""
        return self._id_emprestimo

    @property
    def id_exemplar(self):
        """Getter do ID do exemplar"""
        return self._id_exemplar

    @property
    def id_dono(self):
        """Getter do ID do dono"""
        return self._id_dono

    @property
    def id_emprestado(self):
        """Getter do ID de quem pegou emprestado"""
        return self._id_emprestado

    @property
    def data_inicio(self):
        """Getter da data de início"""
        return self._data_inicio
    
    @data_inicio.setter
    def data_inicio(self, value):
        """Setter com validação da data de início"""
        self._validar_data(value)
        self._data_inicio = value

    @property
    def data_prevista(self):
        """Getter da data prevista de devolução"""
        return self._data_prevista
    
    @data_prevista.setter
    def data_prevista(self, value):
        """Setter com validação da data prevista"""
        self._validar_data(value)
        self._data_prevista = value

    @property
    def data_devolucao(self):
        """Getter da data de devolução"""
        return self._data_devolucao
    
    @data_devolucao.setter
    def data_devolucao(self, value):
        """Setter com validação da data de devolução"""
        if value is not None:
            self._validar_data(value)
        self._data_devolucao = value

    def _validar_data(self, data):
        """Valida formato de data"""
        if isinstance(data, str):
            try:
                datetime.fromisoformat(data)
            except ValueError:
                raise EmprestimoException.DadosInvalidos(
                    "Data deve estar no formato ISO (YYYY-MM-DD)"
                )

    def esta_ativo(self):
        """Verifica se o empréstimo está ativo (não devolvido)"""
        return self.data_devolucao is None

    def esta_atrasado(self):
        """Verifica se o empréstimo está atrasado"""
        if not self.esta_ativo():
            return False
        
        data_prevista = datetime.fromisoformat(self.data_prevista)
        return datetime.now() > data_prevista

    def dias_restantes(self):
        """Calcula dias restantes para devolução"""
        if not self.esta_ativo():
            return 0
        
        data_prevista = datetime.fromisoformat(self.data_prevista)
        dias = (data_prevista - datetime.now()).days
        return max(0, dias)

    def registrar_devolucao(self, data_devolucao=None):
        """Registra a devolução do exemplar"""
        if not self.esta_ativo():
            raise EmprestimoException.EmprestimoInvalido(
                "Empréstimo já foi devolvido"
            )
        
        if data_devolucao is None:
            data_devolucao = datetime.now().strftime("%Y-%m-%d")
        
        self.data_devolucao = data_devolucao

    def __str__(self):
        """Representação em string do empréstimo"""
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
