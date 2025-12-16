"""
Exemplo de uso completo do sistema BookShare
Demonstra CRUD de todas as entidades principais
"""

from database import Database
from models.usuario import Usuario
from models.livro import Livro
from models.exemplar import Exemplar
from models.emprestimo import Emprestimo
from models.solicitacaoemprestimo import SolicitacaoEmprestimo
from models.avaliacaousuario import AvaliacaoUsuario
from DAO.usuarioDAO import UsuarioDAO
from DAO.livroDAO import LivroDAO
from DAO.exemplarDAO import ExemplarDAO
from DAO.emprestimoDAO import EmprestimoDAO
from DAO.solicitacaoemprestimoDAO import SolicitacaoEmprestimoDAO
from DAO.avaliacaousuarioDAO import AvaliacaoUsuarioDAO
from datetime import date, timedelta


def exemplo_usuarios(usuario_dao):
    """Exemplo de operações com usuários"""
    print("\n" + "="*50)
    print("EXEMPLO: USUÁRIOS")
    print("="*50)
    
    # Criar novo usuário
    novo_usuario = Usuario(None, "João Silva", "joao@email.com", "senha123", 28)
    id_usuario = usuario_dao.inserir(novo_usuario)
    print(f"✓ Usuário criado: {novo_usuario} (ID: {id_usuario})")
    
    # Listar usuários
    usuarios = usuario_dao.listar()
    print(f"✓ Total de usuários: {len(usuarios)}")
    
    return id_usuario


def exemplo_livros(livro_dao):
    """Exemplo de operações com livros"""
    print("\n" + "="*50)
    print("EXEMPLO: LIVROS")
    print("="*50)
    
    # Criar novo livro
    novo_livro = Livro(None, "1984", "George Orwell", 328)
    id_livro = livro_dao.inserir(novo_livro)
    print(f"✓ Livro criado: {novo_livro} (ID: {id_livro})")
    
    # Buscar por título
    encontrados = livro_dao.listar_por_titulo("1984")
    print(f"✓ Livros encontrados: {len(encontrados)}")
    
    return id_livro


def exemplo_exemplares(exemplar_dao, id_usuario, id_livro):
    """Exemplo de operações com exemplares"""
    print("\n" + "="*50)
    print("EXEMPLO: EXEMPLARES")
    print("="*50)
    
    # Criar exemplar
    novo_exemplar = Exemplar(None, id_usuario, id_livro, "disponível")
    id_exemplar = exemplar_dao.inserir(novo_exemplar)
    print(f"✓ Exemplar criado: {novo_exemplar} (ID: {id_exemplar})")
    
    # Listar exemplares do usuário
    exemplares_usuario = exemplar_dao.listar_por_usuario(id_usuario)
    print(f"✓ Exemplares do usuário: {len(exemplares_usuario)}")
    
    return id_exemplar


def exemplo_solicitacoes(solicitacao_dao, id_exemplar):
    """Exemplo de operações com solicitações"""
    print("\n" + "="*50)
    print("EXEMPLO: SOLICITAÇÕES DE EMPRÉSTIMO")
    print("="*50)
    
    # Criar solicitação
    nova_solicitacao = SolicitacaoEmprestimo(
        None, 
        id_exemplar, 
        2,  # ID do solicitante
        str(date.today()), 
        "pendente"
    )
    id_solicitacao = solicitacao_dao.inserir(nova_solicitacao)
    print(f"✓ Solicitação criada: {nova_solicitacao} (ID: {id_solicitacao})")
    
    return id_solicitacao


def exemplo_emprestimos(emprestimo_dao, id_exemplar):
    """Exemplo de operações com empréstimos"""
    print("\n" + "="*50)
    print("EXEMPLO: EMPRÉSTIMOS")
    print("="*50)
    
    # Criar empréstimo
    novo_emprestimo = Emprestimo(
        None,
        id_exemplar,
        1,  # ID do dono
        2,  # ID de quem pegou emprestado
        str(date.today()),
        str(date.today() + timedelta(days=14))  # Prazo de 14 dias
    )
    id_emprestimo = emprestimo_dao.inserir(novo_emprestimo)
    print(f"✓ Empréstimo criado: {novo_emprestimo} (ID: {id_emprestimo})")
    
    return id_emprestimo


def exemplo_avaliacoes(avaliacao_dao):
    """Exemplo de operações com avaliações"""
    print("\n" + "="*50)
    print("EXEMPLO: AVALIAÇÕES DE USUÁRIO")
    print("="*50)
    
    # Criar avaliação
    nova_avaliacao = AvaliacaoUsuario(
        None,
        1,  # ID avaliador
        2,  # ID avaliado
        5,  # Nota
        "Ótimo usuário, muito responsável!",
        str(date.today())
    )
    id_avaliacao = avaliacao_dao.inserir(nova_avaliacao)
    print(f"✓ Avaliação criada: {nova_avaliacao} (ID: {id_avaliacao})")


def main():
    """Função principal - executa todos os exemplos"""
    print("\n🚀 EXEMPLO COMPLETO - SISTEMA BOOKSHARE\n")
    
    # Inicializar banco
    db = Database()
    print("✓ Banco de dados inicializado")
    
    # Criar DAOs
    usuario_dao = UsuarioDAO(db.conn)
    livro_dao = LivroDAO(db.conn)
    exemplar_dao = ExemplarDAO(db.conn)
    solicitacao_dao = SolicitacaoEmprestimoDAO(db.conn)
    emprestimo_dao = EmprestimoDAO(db.conn)
    avaliacao_dao = AvaliacaoUsuarioDAO(db.conn)
    
    try:
        # Executar exemplos
        id_usuario = exemplo_usuarios(usuario_dao)
        id_livro = exemplo_livros(livro_dao)
        id_exemplar = exemplo_exemplares(exemplar_dao, id_usuario, id_livro)
        exemplo_solicitacoes(solicitacao_dao, id_exemplar)
        exemplo_emprestimos(emprestimo_dao, id_exemplar)
        exemplo_avaliacoes(avaliacao_dao)
        
        print("\n" + "="*50)
        print("✓ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n✗ Erro durante execução: {e}\n")
    
    finally:
        db.fechar()
        print("✓ Conexão com banco de dados fechada\n")


if __name__ == "__main__":
    main()
