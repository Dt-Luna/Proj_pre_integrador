class SistemaException(Exception):
    pass


class UsuarioException(SistemaException):
    
    class UsuarioNaoEncontrado(SistemaException):
        pass
    
    class UsuarioDuplicado(SistemaException):
        pass
    
    class CredenciaisInvalidas(SistemaException):
        pass
    
    class DadosInvalidos(SistemaException):
        pass


class LivroException(SistemaException):
    
    class LivroNaoEncontrado(SistemaException):
        pass
    
    class LivroDuplicado(SistemaException):
        pass
    
    class DadosInvalidos(SistemaException):
        pass


class ExemplarException(SistemaException):
    
    class ExemplarNaoEncontrado(SistemaException):
        pass
    
    class ExemplarIndisponivel(SistemaException):
        pass
    
    class DadosInvalidos(SistemaException):
        pass


class SolicitacaoException(SistemaException):
    
    class SolicitacaoNaoEncontrada(SistemaException):
        pass
    
    class SolicitacaoInvalida(SistemaException):
        pass
    
    class DadosInvalidos(SistemaException):
        pass


class EmprestimoException(SistemaException):
    
    class EmprestimoNaoEncontrado(SistemaException):
        pass
    
    class EmprestimoAtrasado(SistemaException):
        pass
    
    class DadosInvalidos(SistemaException):
        pass


class AvaliacaoException(SistemaException):
    
    class AvaliacaoNaoEncontrada(SistemaException):
        pass
    
    class AvaliacaoInvalida(SistemaException):
        pass


class DAOException(SistemaException):
    
    class OperacaoFalhou(SistemaException):
        pass
    
    class ConexaoFalhou(SistemaException):
        pass
    
    class IntegridadeDados(SistemaException):
        pass