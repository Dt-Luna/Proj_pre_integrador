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


def teste_usuario(dao_usuario):
    print("\n" + "="*60)
    print("TESTE: USUÁRIO - SALVAR E LER UM OBJETO")
    print("="*60)
    
    try:
        # CREATE
        print("\n✓ Criando um usuário...")
        usuario = Usuario(None, "joao_silva", "senha123", "joao@email.com", 25)
        id_usuario = dao_usuario.inserir(usuario)
        print(f"  ✓ Usuário inserido com ID: {id_usuario}")
        
        # READ
        print("\n✓ Lendo o usuário do banco de dados...")
        usuario_lido = dao_usuario.listar_id(id_usuario)
        
        if usuario_lido:
            print(f"  ✓ Usuário recuperado com sucesso!")
            print(f"    ID: {usuario_lido[0]}")
            print(f"    Username: {usuario_lido[1]}")
            print(f"    Senha: {usuario_lido[2]}")
            print(f"    Idade: {usuario_lido[3]}")
            print(f"    Email: {usuario_lido[4]}")
            print("\n✓ TESTE DE USUÁRIO PASSOU!")
            return True
        else:
            print("  ✗ Usuário não encontrado")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro no teste de usuário: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_livro(dao_livro):
    print("\n" + "="*60)
    print("TESTE: LIVRO - SALVAR E LER UM OBJETO")
    print("="*60)
    
    try:
        # CREATE
        print("\n✓ Criando um livro...")
        livro = Livro(None, "Clean Code", "Robert Martin", 464)
        id_livro = dao_livro.inserir(livro)
        print(f"  ✓ Livro inserido com ID: {id_livro}")
        
        # READ 
        print("\n✓ Lendo o livro do banco de dados...")
        livro_lido = dao_livro.listar_id(id_livro)
        
        if livro_lido:
            print(f"  ✓ Livro recuperado com sucesso!")
            print(f"    ID: {livro_lido[0]}")
            print(f"    Título: {livro_lido[1]}")
            print(f"    Autor: {livro_lido[2]}")
            print(f"    Páginas: {livro_lido[3]}")
            print("\n✓ TESTE DE LIVRO PASSOU!")
            return True
        else:
            print("  ✗ Livro não encontrado")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro no teste de livro: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_exemplar(dao_exemplar):
    print("\n" + "="*60)
    print("TESTE: EXEMPLAR - SALVAR E LER UM OBJETO")
    print("="*60)
    
    try:
        # CREATE 
        print("\n✓ Criando um exemplar...")
        exemplar = Exemplar(None, 1, 1, Exemplar.STATUS_DISPONIVEL)
        id_exemplar = dao_exemplar.inserir(exemplar)
        print(f"  ✓ Exemplar inserido com ID: {id_exemplar}")
        
        # READ 
        print("\n✓ Lendo o exemplar do banco de dados...")
        exemplar_lido = dao_exemplar.listar_id(id_exemplar)
        
        if exemplar_lido:
            print(f"  ✓ Exemplar recuperado com sucesso!")
            print(f"    ID: {exemplar_lido[0]}")
            print(f"    ID Livro: {exemplar_lido[1]}")
            print(f"    ID Usuário: {exemplar_lido[2]}")
            print(f"    Status: {exemplar_lido[3]}")
            print("\n✓ TESTE DE EXEMPLAR PASSOU!")
            return True
        else:
            print("  ✗ Exemplar não encontrado")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro no teste de exemplar: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_emprestimo(dao_emprestimo):
    print("\n" + "="*60)
    print("TESTE: EMPRÉSTIMO - SALVAR E LER UM OBJETO")
    print("="*60)
    
    try:
        data_inicio = datetime.now().strftime("%Y-%m-%d")
        data_prevista = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        # CREATE 
        print("\n✓ Criando um empréstimo...")
        emprestimo = Emprestimo(None, 1, 1, 2, data_inicio, data_prevista)
        id_emprestimo = dao_emprestimo.inserir(emprestimo)
        print(f"  ✓ Empréstimo inserido com ID: {id_emprestimo}")
        
        # READ 
        print("\n✓ Lendo o empréstimo do banco de dados...")
        emprestimo_lido = dao_emprestimo.listar_id(id_emprestimo)
        
        if emprestimo_lido:
            print(f"  ✓ Empréstimo recuperado com sucesso!")
            print(f"    ID: {emprestimo_lido[0]}")
            print(f"    ID Exemplar: {emprestimo_lido[1]}")
            print(f"    ID Usuário (Solicitante): {emprestimo_lido[2]}")
            print(f"    ID Usuário (Proprietário): {emprestimo_lido[3]}")
            print(f"    Data Início: {emprestimo_lido[4]}")
            print(f"    Data Prevista: {emprestimo_lido[5]}")
            print("\n✓ TESTE DE EMPRÉSTIMO PASSOU!")
            return True
        else:
            print("  ✗ Empréstimo não encontrado")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro no teste de empréstimo: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_solicitacao(dao_solicitacao):
    print("\n" + "="*60)
    print("TESTE: SOLICITAÇÃO - SALVAR E LER UM OBJETO")
    print("="*60)
    
    try:
        data_solicitacao = datetime.now().strftime("%Y-%m-%d")
        
        # CREATE 
        print("\n✓ Criando uma solicitação de empréstimo...")
        solicitacao = SolicitacaoEmprestimo(None, 3, 2, data_solicitacao)
        id_solicitacao = dao_solicitacao.inserir(solicitacao)
        print(f"  ✓ Solicitação inserida com ID: {id_solicitacao}")
        
        # READ 
        print("\n✓ Lendo a solicitação do banco de dados...")
        solicitacao_lida = dao_solicitacao.listar_id(id_solicitacao)
        
        if solicitacao_lida:
            print(f"  ✓ Solicitação recuperada com sucesso!")
            print(f"    ID: {solicitacao_lida[0]}")
            print(f"    ID Exemplar: {solicitacao_lida[1]}")
            print(f"    ID Usuário: {solicitacao_lida[2]}")
            print(f"    Data Solicitação: {solicitacao_lida[3]}")
            print(f"    Status: {solicitacao_lida[4]}")
            print("\n✓ TESTE DE SOLICITAÇÃO PASSOU!")
            return True
        else:
            print("  ✗ Solicitação não encontrada")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro no teste de solicitação: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_avaliacao(dao_avaliacao):
    print("\n" + "="*60)
    print("TESTE: AVALIAÇÃO - SALVAR E LER UM OBJETO")
    print("="*60)
    
    try:
        data_avaliacao = datetime.now().strftime("%Y-%m-%d")
        
        # CREATE 
        print("\n✓ Criando uma avaliação de usuário...")
        avaliacao = AvaliacaoUsuario(None, 1, 2, 5, "Excelente pessoa!", data_avaliacao)
        id_avaliacao = dao_avaliacao.inserir(avaliacao)
        print(f"  ✓ Avaliação inserida com ID: {id_avaliacao}")
        
        # READ 
        print("\n✓ Lendo a avaliação do banco de dados...")
        avaliacao_lida = dao_avaliacao.listar_id(id_avaliacao)
        
        if avaliacao_lida:
            print(f"  ✓ Avaliação recuperada com sucesso!")
            print(f"    ID: {avaliacao_lida[0]}")
            print(f"    ID Avaliador: {avaliacao_lida[1]}")
            print(f"    ID Avaliado: {avaliacao_lida[2]}")
            print(f"    Nota: {avaliacao_lida[3]}/5")
            print(f"    Comentário: {avaliacao_lida[4]}")
            print(f"    Data: {avaliacao_lida[5]}")
            print("\n✓ TESTE DE AVALIAÇÃO PASSOU!")
            return True
        else:
            print("  ✗ Avaliação não encontrada")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro no teste de avaliação: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("TESTES DO SISTEMA BOOKSHARE")
    print("Teste simples de CRUD para cada classe do modelo")
    print("="*60)
    
    print("\n✓ Conectando ao banco de dados...")
    try:
        db = Database()
    except Exception as e:
        print(f"✗ Erro ao conectar ao banco: {e}")
        return
    
    print("✓ Limpando dados anteriores...")
    try:
        db.limpar_dados()
    except Exception as e:
        print(f"✗ Erro ao limpar dados: {e}")
        return
    
    print("✓ Inicializando DAOs...")
    dao_usuario = UsuarioDAO(db.conn)
    dao_livro = LivroDAO(db.conn)
    dao_exemplar = ExemplarDAO(db.conn)
    dao_emprestimo = EmprestimoDAO(db.conn)
    dao_solicitacao = SolicitacaoEmprestimoDAO(db.conn)
    dao_avaliacao = AvaliacaoUsuarioDAO(db.conn)
    
    # Executar testes
    resultados = []
    resultados.append(("Usuário", teste_usuario(dao_usuario)))
    resultados.append(("Livro", teste_livro(dao_livro)))
    resultados.append(("Exemplar", teste_exemplar(dao_exemplar)))
    resultados.append(("Empréstimo", teste_emprestimo(dao_emprestimo)))
    resultados.append(("Solicitação", teste_solicitacao(dao_solicitacao)))
    resultados.append(("Avaliação", teste_avaliacao(dao_avaliacao)))
    
    # Resumo dos resultados
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    passou = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"{nome:.<40} {status}")
    
    print(f"\nTotal: {passou}/{total} testes passaram")
    
    if passou == total:
        print("\nTODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print(f"\n{total - passou} teste(s) falharam")
    
    db.fechar()


if __name__ == "__main__":
    main()