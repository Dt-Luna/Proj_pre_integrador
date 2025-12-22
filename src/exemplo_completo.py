import sys
from datetime import date, timedelta

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

from models.autenticacao import SistemaAutenticacao
from exceptions import SistemaException, UsuarioException, LivroException


def exibir_titulo(titulo):
    print("\n" + "="*60)
    print(f"  {titulo.upper()}")
    print("="*60 + "\n")


def exemplo_validacao_encapsulamento():
    exibir_titulo("1. Validação e Encapsulamento dos Modelos")
    
    print("📋 Testando validação de usuário:")
    
    # Teste 1: Usuário válido
    try:
        usuario_valido = Usuario(1, "joao_silva", "senha123", "joao@email.com", 25)
        print(f"  ✓ Usuário válido criado: {usuario_valido}")
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    # Teste 2: Username inválido (muito curto)
    print("\n  Testando username inválido (< 3 caracteres):")
    try:
        usuario_invalido = Usuario(2, "ab", "senha123", "teste@email.com", 25)
    except UsuarioException.DadosInvalidos as e:
        print(f"  ✓ Validação funcionou: {e}")
    
    # Teste 3: Email inválido
    print("\n  Testando email inválido:")
    try:
        usuario_invalido = Usuario(3, "maria_santos", "senha123", "emailinvalido", 25)
    except UsuarioException.DadosInvalidos as e:
        print(f"  ✓ Validação funcionou: {e}")
    
    # Teste 4: Idade inválida
    print("\n  Testando idade inválida:")
    try:
        usuario_invalido = Usuario(4, "carlos_silva", "senha123", "carlos@email.com", 10)
    except UsuarioException.DadosInvalidos as e:
        print(f"  ✓ Validação funcionou: {e}")


def exemplo_usuarios(usuario_dao):
    exibir_titulo("2. Operações CRUD - Usuários")
    
    # CREATE - Inserir usuários
    print("📝 Criando novos usuários:\n")
    usuarios_criados = []
    
    import time
    ts = int(time.time())
    usuarios_dados = [
        (f"joao_silva_{ts}", f"joao_{ts}@email.com", 28, "senha123"),
        (f"maria_santos_{ts}", f"maria_{ts}@email.com", 25, "senha456"),
        (f"carlos_costa_{ts}", f"carlos_{ts}@email.com", 32, "senha789")
    ]
    
    for username, email, idade, senha in usuarios_dados:
        try:
            novo_usuario = Usuario(None, username, senha, email, idade)
            id_usuario = usuario_dao.inserir(novo_usuario)
            usuarios_criados.append(id_usuario)
            print(f"  ✓ Usuário '{username}' criado com ID: {id_usuario}")
        except SistemaException as e:
            print(f"  ✗ Erro ao criar usuário: {e}")
    
    # READ - Listar usuários
    print("\n📖 Listando todos os usuários:\n")
    try:
        usuarios = usuario_dao.listar()
        print(f"  Total de usuários: {len(usuarios)}\n")
        print(f"  {'ID':<5} {'Username':<15} {'Email':<25} {'Idade':<5}")
        print("  " + "-" * 55)
        for usuario in usuarios:
            id_u, username, _, idade, email = usuario
            print(f"  {id_u:<5} {username:<15} {email:<25} {idade:<5}")
    except SistemaException as e:
        print(f"  ✗ Erro ao listar: {e}")
    
    # READ - Buscar por ID
    if usuarios_criados:
        print(f"\n🔍 Buscando usuário por ID ({usuarios_criados[0]}):\n")
        try:
            usuario = usuario_dao.listar_por_id(usuarios_criados[0])
            if usuario:
                id_u, username, _, idade, email = usuario
                print(f"  ✓ Usuário encontrado: {username}")
                print(f"    Email: {email}")
                print(f"    Idade: {idade}")
        except SistemaException as e:
            print(f"  ✗ Erro: {e}")
    
    # UPDATE - Atualizar usuário
    if usuarios_criados:
        print(f"\n✏️  Atualizando usuário (ID: {usuarios_criados[0]}):\n")
        try:
            import time
            ts = int(time.time())
            usuario_atualizado = Usuario(
                usuarios_criados[0], 
                f"joao_silva_atualizado_{ts}",
                "nova_senha123",
                f"joao_novo_{ts}@email.com",
                29
            )
            if usuario_dao.atualizar(usuario_atualizado):
                print(f"  ✓ Usuário atualizado com sucesso")
        except SistemaException as e:
            print(f"  ✗ Erro ao atualizar: {e}")
    
    return usuarios_criados


def exemplo_livros(livro_dao, usuario_dao):
    """Demonstra CRUD de livros"""
    exibir_titulo("3. Operações CRUD - Livros")
    
    print("📚 Criando novos livros:\n")
    livros_criados = []
    
    livros_dados = [
        ("1984", "George Orwell", 328),
        ("Dom Casmurro", "Machado de Assis", 272),
        ("O Cortiço", "Aluísio Azevedo", 384)
    ]
    
    for titulo, autor, paginas in livros_dados:
        try:
            novo_livro = Livro(None, titulo, autor, paginas)
            id_livro = livro_dao.inserir(novo_livro)
            livros_criados.append(id_livro)
            print(f"  ✓ Livro '{titulo}' criado com ID: {id_livro}")
        except SistemaException as e:
            print(f"  ✗ Erro ao criar livro: {e}")
    
    print("\n📖 Listando todos os livros:\n")
    try:
        livros = livro_dao.listar()
        print(f"  Total de livros: {len(livros)}\n")
        print(f"  {'ID':<5} {'Título':<25} {'Autor':<20} {'Páginas':<8}")
        print("  " + "-" * 60)
        for livro in livros:
            id_l, titulo, autor, paginas, _ = livro
            print(f"  {id_l:<5} {titulo:<25} {autor:<20} {paginas:<8}")
    except SistemaException as e:
        print(f"  ✗ Erro ao listar: {e}")
    
    return livros_criados


def exemplo_exemplares(exemplar_dao, usuario_id, livro_id):
    exibir_titulo("4. Operações CRUD - Exemplares")
    
    print("📚 Criando exemplares de livros:\n")
    exemplares_criados = []
    
    # Criar exemplares com status válido
    try:
        novo_exemplar = Exemplar(
            None, 
            usuario_id, 
            livro_id, 
            Exemplar.STATUS_DISPONIVEL
        )
        id_exemplar = exemplar_dao.inserir(novo_exemplar)
        exemplares_criados.append(id_exemplar)
        print(f"  ✓ Exemplar criado com ID: {id_exemplar}")
        print(f"    Status: {novo_exemplar.status}")
    except SistemaException as e:
        print(f"  ✗ Erro ao criar exemplar: {e}")
    
    # Demonstrar mudança de status
    if exemplares_criados:
        print(f"\n🔄 Testando mudança de status do exemplar:\n")
        try:
            exemplar = exemplar_dao.listar_por_id(exemplares_criados[0])
            if exemplar:
                id_ex, id_usr, id_liv, status = exemplar
                
                # Simulando empréstimo
                novo_exemplar = Exemplar(id_ex, id_usr, id_liv, status)
                print(f"  Status inicial: {novo_exemplar.status}")
                
                # Emprestar
                novo_exemplar.emprestar()
                print(f"  ✓ Exemplar emprestado. Novo status: {novo_exemplar.status}")
                
                # Devolver
                novo_exemplar.devolver()
                print(f"  ✓ Exemplar devolvido. Novo status: {novo_exemplar.status}")
        except SistemaException as e:
            print(f"  ✗ Erro: {e}")
    
    return exemplares_criados


def exemplo_emprestimos(emprestimo_dao, exemplar_id, usuario_dono, usuario_devedor):
    exibir_titulo("5. Operações CRUD - Empréstimos")
    
    print("📞 Criando empréstimos:\n")
    
    try:
        novo_emprestimo = Emprestimo(
            None,
            exemplar_id,
            usuario_dono,
            usuario_devedor,
            date.today().isoformat(),
            (date.today() + timedelta(days=14)).isoformat()
        )
        
        id_emprestimo = emprestimo_dao.inserir(novo_emprestimo)
        print(f"  ✓ Empréstimo criado com ID: {id_emprestimo}")
        print(f"    Exemplar: {exemplar_id}")
        print(f"    Data de início: {novo_emprestimo.data_inicio}")
        print(f"    Data prevista: {novo_emprestimo.data_prevista}")
        print(f"    Status: {'Ativo' if novo_emprestimo.esta_ativo() else 'Devolvido'}")
        print(f"    Dias restantes: {novo_emprestimo.dias_restantes()}")
        
        return id_emprestimo
    except SistemaException as e:
        print(f"  ✗ Erro ao criar empréstimo: {e}")
        return None


def exemplo_solicitacoes(solicitacao_dao, exemplar_id, solicitante_id):
    exibir_titulo("6. Operações CRUD - Solicitações de Empréstimo")
    
    print("📋 Criando solicitação de empréstimo:\n")
    
    try:
        nova_solicitacao = SolicitacaoEmprestimo(
            None,
            exemplar_id,
            solicitante_id,
            date.today().isoformat(),
            SolicitacaoEmprestimo.STATUS_PENDENTE
        )
        
        id_solicitacao = solicitacao_dao.inserir(nova_solicitacao)
        print(f"  ✓ Solicitação criada com ID: {id_solicitacao}")
        print(f"    Status: {nova_solicitacao.status}")
        print(f"    Data: {nova_solicitacao.data}")
        
        # Demonstrar transições de estado
        print(f"\n🔄 Testando transições de estado:\n")
        nova_solicitacao.aceitar()
        print(f"  ✓ Solicitação aceita. Status: {nova_solicitacao.status}")
        
        return id_solicitacao
    except SistemaException as e:
        print(f"  ✗ Erro: {e}")
        return None


def exemplo_avaliacoes(avaliacao_dao, avaliador_id, avaliado_id):
    exibir_titulo("7. Operações CRUD - Avaliações de Usuário")
    
    print("⭐ Criando avaliação:\n")
    
    try:
        nova_avaliacao = AvaliacaoUsuario(
            None,
            avaliador_id,
            avaliado_id,
            5,
            "Ótimo usuário! Muito responsável e confiável.",
            date.today().isoformat()
        )
        
        id_avaliacao = avaliacao_dao.inserir(nova_avaliacao)
        print(f"  ✓ Avaliação criada com ID: {id_avaliacao}")
        print(f"    Nota: {nova_avaliacao.nota}/5")
        print(f"    Comentário: {nova_avaliacao.comentario}")
        
        return id_avaliacao
    except SistemaException as e:
        print(f"  ✗ Erro: {e}")
        return None


def exemplo_autenticacao(usuario_dao):
    exibir_titulo("8. Sistema de Autenticação")
    
    print("🔐 Testando login e logout:\n")
    
    # Criar sistema de autenticação
    autenticacao = SistemaAutenticacao(usuario_dao)
    
    # Obter primeiro usuário criado
    usuarios = usuario_dao.listar()
    if usuarios:
        id_u, username, senha, idade, email = usuarios[0]
        
        # Teste 1: Login bem-sucedido
        try:
            autenticacao.fazer_login(username, senha)
            usuario = autenticacao.obter_usuario_logado()
            print(f"  ✓ Login realizado: {usuario['username']}")
            print(f"    Email: {usuario['email']}")
            print(f"    ID: {usuario['id']}")
        except SistemaException as e:
            print(f"  ✗ Erro: {e}")
        
        # Teste 2: Logout
        autenticacao.fazer_logout()
        print(f"\n  ✓ Logout realizado")
        print(f"    Usuário logado: {autenticacao.esta_logado()}")
        
        # Teste 3: Credenciais inválidas
        print(f"\n  Testando credenciais inválidas:\n")
        try:
            autenticacao.fazer_login(username, "senha_errada")
        except UsuarioException.CredenciaisInvalidas as e:
            print(f"  ✓ Validação funcionou: {e}")
        except Exception as e:
            print(f"  ✓ Validação funcionou: {type(e).__name__}")


def main():
    print("\n" + "="*60)
    print("  BOOKSHARE - Sistema de Empréstimo de Livros")
    print("  Implementação de Modelos e Persistência com Validação")
    print("="*60)
    
    # Inicializar banco de dados
    try:
        db = Database()
        print("\n✓ Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"\n✗ Erro ao inicializar banco: {e}")
        sys.exit(1)
    
    # Criar DAOs com injeção de conexão (padrão correto)
    usuario_dao = UsuarioDAO(db.conn)
    livro_dao = LivroDAO(db.conn)
    exemplar_dao = ExemplarDAO(db.conn)
    emprestimo_dao = EmprestimoDAO(db.conn)
    solicitacao_dao = SolicitacaoEmprestimoDAO(db.conn)
    avaliacao_dao = AvaliacaoUsuarioDAO(db.conn)
    
    try:
        # Executar exemplos
        exemplo_validacao_encapsulamento()
        
        usuarios = exemplo_usuarios(usuario_dao)
        livros = exemplo_livros(livro_dao, usuario_dao)
        exemplares = exemplo_exemplares(exemplar_dao, usuarios[0], livros[0])
        exemplo_emprestimos(emprestimo_dao, exemplares[0], usuarios[0], usuarios[1])
        exemplo_solicitacoes(solicitacao_dao, exemplares[0], usuarios[1])
        exemplo_avaliacoes(avaliacao_dao, usuarios[0], usuarios[1])
        exemplo_autenticacao(usuario_dao)
        
    except Exception as e:
        print(f"\n✗ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.fechar()
        print("\n✓ Banco de dados fechado\n")

if __name__ == "__main__":
    main()