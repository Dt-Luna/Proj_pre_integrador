"""
Módulo de Exceções Customizadas do Sistema de Agendamento de Serviços
Segue o padrão de encapsulamento e tratamento de erros do sistema
"""


class SistemaException(Exception):
    """Exceção base para o sistema"""
    pass


class UsuarioException(SistemaException):
    """Exceção relacionada a operações com Usuários"""
    
    class UsuarioNaoEncontrado(SistemaException):
        """Usuário não encontrado no sistema"""
        pass
    
    class UsuarioDuplicado(SistemaException):
        """Usuário duplicado (email ou username já existe)"""
        pass
    
    class CredenciaisInvalidas(SistemaException):
        """Credenciais de autenticação inválidas"""
        pass
    
    class DadosInvalidos(SistemaException):
        """Dados do usuário inválidos"""
        pass


class LivroException(SistemaException):
    """Exceção relacionada a operações com Livros"""
    
    class LivroNaoEncontrado(SistemaException):
        """Livro não encontrado no sistema"""
        pass
    
    class LivroDuplicado(SistemaException):
        """Livro já existe no sistema"""
        pass
    
    class DadosInvalidos(SistemaException):
        """Dados do livro inválidos"""
        pass


class ExemplarException(SistemaException):
    """Exceção relacionada a operações com Exemplares"""
    
    class ExemplarNaoEncontrado(SistemaException):
        """Exemplar não encontrado no sistema"""
        pass
    
    class ExemplarIndisponivel(SistemaException):
        """Exemplar não está disponível para empréstimo"""
        pass
    
    class DadosInvalidos(SistemaException):
        """Dados do exemplar inválidos"""
        pass


class SolicitacaoException(SistemaException):
    """Exceção relacionada a operações com Solicitações"""
    
    class SolicitacaoNaoEncontrada(SistemaException):
        """Solicitação não encontrada no sistema"""
        pass
    
    class SolicitacaoInvalida(SistemaException):
        """Solicitação em estado inválido para a operação"""
        pass
    
    class DadosInvalidos(SistemaException):
        """Dados da solicitação inválidos"""
        pass


class EmprestimoException(SistemaException):
    """Exceção relacionada a operações com Empréstimos"""
    
    class EmprestimoNaoEncontrado(SistemaException):
        """Empréstimo não encontrado no sistema"""
        pass
    
    class EmprestimoAtrasado(SistemaException):
        """Empréstimo encontra-se atrasado"""
        pass
    
    class DadosInvalidos(SistemaException):
        """Dados do empréstimo inválidos"""
        pass


class AvaliacaoException(SistemaException):
    """Exceção relacionada a operações com Avaliações"""
    
    class AvaliacaoNaoEncontrada(SistemaException):
        """Avaliação não encontrada no sistema"""
        pass
    
    class AvaliacaoInvalida(SistemaException):
        """Dados da avaliação inválidos"""
        pass


class DAOException(SistemaException):
    """Exceção relacionada a operações de Persistência"""
    
    class OperacaoFalhou(SistemaException):
        """Operação de banco de dados falhou"""
        pass
    
    class ConexaoFalhou(SistemaException):
        """Falha ao conectar ao banco de dados"""
        pass
    
    class IntegridadeDados(SistemaException):
        """Violação de integridade de dados"""
        pass
