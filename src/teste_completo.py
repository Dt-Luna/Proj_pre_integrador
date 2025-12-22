import sys
from datetime import datetime, timedelta
from database import Database
from models.usuario import Usuario, UsuarioDAO
from models.livro import Livro, LivroDAO
from models.exemplar import Exemplar, ExemplarDAO
from models.emprestimo import Emprestimo, EmprestimoDAO
from models.solicitacaoemprestimo import SolicitacaoEmprestimo, SolicitacaoEmprestimoDAO
from models.avaliacaousuario import AvaliacaoUsuario, AvaliacaoUsuarioDAO
from models.historicoemprestimos import HistoricoEmprestimos, HistoricoEmprestimosDAO
from exceptions import *


def teste_usuarios(dao_usuario):
    print("\n" + "="*60)
    print("TESTE 1: USUÁRIOS (CRUD)")
    print("="*60)
    
    try:
        # CREATE
        print("\n✓ Inserindo usuários...")
        u1 = Usuario(None, "joao_silva", "senha123", "joao@email.com", 25)
        u2 = Usuario(None, "maria_santos", "senha456", "maria@email.com", 30)
        
        id1 = dao_usuario.inserir(u1)
        id2 = dao_usuario.inserir(u2)
        print(f"  Usuário João inserido com ID: {id1}")
        print(f"  Usuária Maria inserida com ID: {id2}")
        
        # READ
        print("\n✓ Listando todos os usuários...")
        usuarios = dao_usuario.listar()
        print(f"  Total de usuários: {len(usuarios)}")
        for u in usuarios:
            print(f"    ID: {u[0]}, Username: {u[1]}, Email: {u[3]}, Idade: {u[4]}")
        
        # READ by ID
        print("\n✓ Buscando usuário por ID...")
        usuario = dao_usuario.listar_id(1)
        if usuario:
            print(f"  Encontrado: {usuario[1]} ({usuario[3]})")
        
        # UPDATE
        print("\n✓ Atualizando usuário...")
        u1.set_id(1)
        u1.set_idade(26)
        dao_usuario.atualizar(u1)
        usuario_atualizado = dao_usuario.listar_id(1)
        print(f"  Idade atualizada para: {usuario_atualizado[4]}")
        
        # AUTENTICAÇÃO
        print("\n✓ Testando autenticação...")
        try:
            resultado = dao_usuario.autenticar("joao_silva", "senha123")
            print(f"  ✓ Autenticação bem-sucedida para: {resultado[1]}")
        except UsuarioException.CredenciaisInvalidas as e:
            print(f"  ✗ Erro: {e}")
        
        print("\n✓ Testes de usuários PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de usuários: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_livros(dao_livro):
    print("\n" + "="*60)
    print("TESTE 2: LIVROS (CRUD)")
    print("="*60)
    
    try:
        # CREATE
        print("\n✓ Inserindo livros...")
        l1 = Livro(None, "Clean Code", "Robert Martin", 464)
        l2 = Livro(None, "Design Patterns", "Gang of Four", 395)
        
        id1 = dao_livro.inserir(l1)
        id2 = dao_livro.inserir(l2)
        print(f"  Livro 'Clean Code' inserido com ID: {id1}")
        print(f"  Livro 'Design Patterns' inserido com ID: {id2}")
        
        # READ
        print("\n✓ Listando todos os livros...")
        livros = dao_livro.listar()
        print(f"  Total de livros: {len(livros)}")
        for l in livros:
            print(f"    ID: {l[0]}, Título: {l[1]}, Autor: {l[2]}, Páginas: {l[3]}")
        
        # READ by AUTHOR
        print("\n✓ Buscando livros por autor...")
        livros_author = dao_livro.listar_por_autor("Robert Martin")
        for l in livros_author:
            print(f"    Encontrado: {l[1]} por {l[2]}")
        
        # UPDATE
        print("\n✓ Atualizando livro...")
        l1.set_id(1)
        l1.set_paginas(500)
        dao_livro.atualizar(l1)
        livro_atualizado = dao_livro.listar_id(1)
        print(f"  Páginas atualizadas para: {livro_atualizado[3]}")
        
        print("\n✓ Testes de livros PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de livros: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_exemplares(dao_exemplar):
    print("\n" + "="*60)
    print("TESTE 3: EXEMPLARES")
    print("="*60)
    
    try:
        # CREATE
        print("\n✓ Inserindo exemplares...")
        ex1 = Exemplar(None, 1, 1, Exemplar.STATUS_DISPONIVEL)
        ex2 = Exemplar(None, 1, 2, Exemplar.STATUS_DISPONIVEL)
        ex3 = Exemplar(None, 2, 1, Exemplar.STATUS_DISPONIVEL)
        
        id1 = dao_exemplar.inserir(ex1)
        id2 = dao_exemplar.inserir(ex2)
        id3 = dao_exemplar.inserir(ex3)
        print(f"  Exemplar 1 inserido com ID: {id1}")
        print(f"  Exemplar 2 inserido com ID: {id2}")
        print(f"  Exemplar 3 inserido com ID: {id3}")
        
        # READ
        print("\n✓ Listando exemplares do usuário 1...")
        exemplares = dao_exemplar.listar_por_usuario(1)
        print(f"  Total: {len(exemplares)}")
        for e in exemplares:
            print(f"    ID: {e[0]}, Livro: {e[2]}, Status: {e[3]}")
        
        # MUDAR STATUS
        print("\n✓ Testando mudanças de status...")
        ex1.set_id(1)
        ex1.emprestar()
        dao_exemplar.atualizar(ex1)
        exemplar_atualizado = dao_exemplar.listar_id(1)
        print(f"  Status do exemplar 1 atualizado para: {exemplar_atualizado[3]}")
        
        print("\n✓ Testes de exemplares PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de exemplares: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_emprestimos(dao_emprestimo):
    print("\n" + "="*60)
    print("TESTE 4: EMPRÉSTIMOS")
    print("="*60)
    
    try:
        data_inicio = datetime.now().strftime("%Y-%m-%d")
        data_prevista = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        # CREATE
        print("\n✓ Inserindo empréstimos...")
        emp1 = Emprestimo(None, 1, 1, 2, data_inicio, data_prevista)
        emp2 = Emprestimo(None, 2, 1, 2, data_inicio, data_prevista)
        
        id1 = dao_emprestimo.inserir(emp1)
        id2 = dao_emprestimo.inserir(emp2)
        print(f"  Empréstimo 1 inserido com ID: {id1}")
        print(f"  Empréstimo 2 inserido com ID: {id2}")
        
        # READ
        print("\n✓ Listando empréstimos...")
        emprestimos = dao_emprestimo.listar()
        print(f"  Total: {len(emprestimos)}")
        for e in emprestimos:
            status = "Ativo" if e[6] is None else "Devolvido"
            print(f"    ID: {e[0]}, Exemplar: {e[1]}, Status: {status}")
        
        # REGISTRAR DEVOLUÇÃO
        print("\n✓ Testando devolução de empréstimo...")
        emp1.set_id(1)
        emp1.registrar_devolucao()
        dao_emprestimo.atualizar(emp1)
        emprestimo_atualizado = dao_emprestimo.listar_id(1)
        print(f"  Data de devolução registrada: {emprestimo_atualizado[6]}")
        
        print("\n✓ Testes de empréstimos PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de empréstimos: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_solicitacoes(dao_solicitacao):
    print("\n" + "="*60)
    print("TESTE 5: SOLICITAÇÕES DE EMPRÉSTIMO")
    print("="*60)
    
    try:
        data_solicitacao = datetime.now().strftime("%Y-%m-%d")
        
        # CREATE
        print("\n✓ Inserindo solicitações...")
        sol1 = SolicitacaoEmprestimo(None, 3, 2, data_solicitacao)
        sol2 = SolicitacaoEmprestimo(None, 2, 1, data_solicitacao)
        
        id1 = dao_solicitacao.inserir(sol1)
        id2 = dao_solicitacao.inserir(sol2)
        print(f"  Solicitação 1 inserida com ID: {id1}")
        print(f"  Solicitação 2 inserida com ID: {id2}")
        
        # READ
        print("\n✓ Listando solicitações...")
        solicitacoes = dao_solicitacao.listar()
        print(f"  Total: {len(solicitacoes)}")
        for s in solicitacoes:
            print(f"    ID: {s[0]}, Exemplar: {s[1]}, Status: {s[4]}")
        
        # MUDAR STATUS
        print("\n✓ Testando mudanças de status...")
        sol1.set_id(1)
        sol1.aceitar()
        dao_solicitacao.atualizar(sol1)
        solicitacao_atualizada = dao_solicitacao.listar_id(1)
        print(f"  Status da solicitação 1 atualizado para: {solicitacao_atualizada[4]}")
        
        print("\n✓ Testes de solicitações PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de solicitações: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_avaliacoes(dao_avaliacao):
    print("\n" + "="*60)
    print("TESTE 6: AVALIAÇÕES DE USUÁRIOS")
    print("="*60)
    
    try:
        data_avaliacao = datetime.now().strftime("%Y-%m-%d")
        
        # CREATE
        print("\n✓ Inserindo avaliações...")
        av1 = AvaliacaoUsuario(None, 1, 2, 5, "Excelente pessoa!", data_avaliacao)
        av2 = AvaliacaoUsuario(None, 2, 1, 4, "Muito bom!", data_avaliacao)
        
        id1 = dao_avaliacao.inserir(av1)
        id2 = dao_avaliacao.inserir(av2)
        print(f"  Avaliação 1 inserida com ID: {id1}")
        print(f"  Avaliação 2 inserida com ID: {id2}")
        
        # READ
        print("\n✓ Listando avaliações...")
        avaliacoes = dao_avaliacao.listar()
        print(f"  Total: {len(avaliacoes)}")
        for a in avaliacoes:
            print(f"    ID: {a[0]}, Nota: {a[3]}/5, Comentário: {a[4]}")
        
        # UPDATE
        print("\n✓ Atualizando avaliação...")
        av1.set_id(1)
        av1.set_nota(4)
        av1.set_comentario("Muito bom!")
        dao_avaliacao.atualizar(av1)
        avaliacao_atualizada = dao_avaliacao.listar_id(1)
        print(f"  Avaliação 1 atualizada: {avaliacao_atualizada[3]}/5")
        
        print("\n✓ Testes de avaliações PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de avaliações: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_historico(dao_historico):
    print("\n" + "="*60)
    print("TESTE 7: HISTÓRICO DE EMPRÉSTIMOS")
    print("="*60)
    
    try:
        # CREATE
        print("\n✓ Inserindo registros de histórico...")
        hist1 = HistoricoEmprestimos(None, 1, HistoricoEmprestimos.STATUS_CONCLUIDO)
        hist2 = HistoricoEmprestimos(None, 2, HistoricoEmprestimos.STATUS_ATIVO)
        
        id1 = dao_historico.inserir(hist1)
        id2 = dao_historico.inserir(hist2)
        print(f"  Histórico 1 inserido com ID: {id1}")
        print(f"  Histórico 2 inserido com ID: {id2}")
        
        # READ
        print("\n✓ Listando histórico...")
        historicos = dao_historico.listar()
        print(f"  Total: {len(historicos)}")
        for h in historicos:
            print(f"    ID: {h[0]}, Empréstimo: {h[1]}, Status: {h[2]}")
        
        # UPDATE
        print("\n✓ Atualizando histórico...")
        hist2.set_id(2)
        hist2.set_status_final(HistoricoEmprestimos.STATUS_CONCLUIDO)
        dao_historico.atualizar(hist2)
        historico_atualizado = dao_historico.listar_id(2)
        print(f"  Histórico 2 atualizado: {historico_atualizado[2]}")
        
        print("\n✓ Testes de histórico PASSOU!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro no teste de histórico: {e}")
        import traceback
        traceback.print_exc()
        return False


def teste_validacoes():
    print("\n" + "="*60)
    print("TESTE 8: VALIDAÇÕES DOS MODELOS")
    print("="*60)
    
    testes_passados = 0
    testes_totais = 0
    
    testes_totais += 1
    print("\n✓ Testando validações de Usuario...")
    try:
        Usuario(None, "ab", "senha", "email@test.com", 25)  
        print("  ✗ Deveria ter lançado exceção")
    except UsuarioException.DadosInvalidos:
        print("  ✓ Username curto rejeitado corretamente")
        testes_passados += 1
    
    testes_totais += 1
    try:
        Usuario(None, "usuario", "123", "email@test.com", 25)  
        print("  ✗ Deveria ter lançado exceção")
    except UsuarioException.DadosInvalidos:
        print("  ✓ Senha curta rejeitada corretamente")
        testes_passados += 1
    
    testes_totais += 1
    try:
        Usuario(None, "usuario", "senha123", "email_invalido", 25)  
        print("  ✗ Deveria ter lançado exceção")
    except UsuarioException.DadosInvalidos:
        print("  ✓ Email inválido rejeitado corretamente")
        testes_passados += 1
    
    testes_totais += 1
    print("\n✓ Testando validações de Livro...")
    try:
        Livro(None, "", "Autor", 100)  
        print("  ✗ Deveria ter lançado exceção")
    except LivroException.DadosInvalidos:
        print("  ✓ Título vazio rejeitado corretamente")
        testes_passados += 1
    
    testes_totais += 1
    try:
        Livro(None, "Título", "Autor", 0)  
        print("  ✗ Deveria ter lançado exceção")
    except LivroException.DadosInvalidos:
        print("  ✓ Páginas inválidas rejeitadas corretamente")
        testes_passados += 1
    
    testes_totais += 1
    print("\n✓ Testando validações de AvaliacaoUsuario...")
    try:
        AvaliacaoUsuario(None, 1, 2, 10, "Comentário", "2024-01-01")  
        print("  ✗ Deveria ter lançado exceção")
    except AvaliacaoException.AvaliacaoInvalida:
        print("  ✓ Nota acima do máximo rejeitada corretamente")
        testes_passados += 1
    
    print(f"\n✓ Testes de validações: {testes_passados}/{testes_totais} PASSOU!")
    return testes_passados == testes_totais


def main():
    print("\n" + "="*60)
    print("TESTES DO SISTEMA BOOKSHARE")
    print("="*60)
    
    print("\n✓ Conectando ao banco de dados...")
    try:
        db = Database()
    except Exception as e:
        print(f"✗ Erro ao conectar ao banco: {e}")
        return
    
    print("✓ Inicializando DAOs...")
    dao_usuario = UsuarioDAO(db.conn)
    dao_livro = LivroDAO(db.conn)
    dao_exemplar = ExemplarDAO(db.conn)
    dao_emprestimo = EmprestimoDAO(db.conn)
    dao_solicitacao = SolicitacaoEmprestimoDAO(db.conn)
    dao_avaliacao = AvaliacaoUsuarioDAO(db.conn)
    dao_historico = HistoricoEmprestimosDAO(db.conn)
    
    # Executar testes
    resultados = []
    resultados.append(("Usuários", teste_usuarios(dao_usuario)))
    resultados.append(("Livros", teste_livros(dao_livro)))
    resultados.append(("Exemplares", teste_exemplares(dao_exemplar)))
    resultados.append(("Empréstimos", teste_emprestimos(dao_emprestimo)))
    resultados.append(("Solicitações", teste_solicitacoes(dao_solicitacao)))
    resultados.append(("Avaliações", teste_avaliacoes(dao_avaliacao)))
    resultados.append(("Histórico", teste_historico(dao_historico)))
    resultados.append(("Validações", teste_validacoes()))
    
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
        print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print(f"\n⚠️  {total - passou} teste(s) falharam")
    
    db.fechar()


if __name__ == "__main__":
    main()