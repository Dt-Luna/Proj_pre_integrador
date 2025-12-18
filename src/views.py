class View:
    
    @staticmethod
    def limpar_tela():
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def exibir_titulo(titulo):
        print("\n" + "=" * 60)
        print(f"  {titulo.upper()}")
        print("=" * 60 + "\n")
    
    @staticmethod
    def exibir_secao(secao):
        print(f"\n--- {secao} ---\n")
    
    @staticmethod
    def exibir_sucesso(mensagem):
        print(f"✓ {mensagem}")
    
    @staticmethod
    def exibir_erro(mensagem):
        print(f"✗ Erro: {mensagem}")
    
    @staticmethod
    def exibir_aviso(mensagem):
        print(f"⚠ {mensagem}")
    
    @staticmethod
    def exibir_menu(opcoes):
        for i, opcao in enumerate(opcoes, 1):
            print(f"{i}. {opcao}")
        print(f"{len(opcoes) + 1}. Sair")
        return input("\nEscolha uma opção: ")
    
    @staticmethod
    def input_com_validacao(mensagem, tipo=str):
        while True:
            try:
                valor = input(f"{mensagem}: ")
                if tipo == int:
                    return int(valor)
                elif tipo == float:
                    return float(valor)
                else:
                    return valor
            except ValueError:
                print(f"Valor inválido! Digite um {tipo.__name__}")


class MenuPrincipal(View):
    
    @staticmethod
    def exibir():
        View.limpar_tela()
        View.exibir_titulo("Sistema de Empréstimo de Livros - BookShare")
        
        opcoes = [
            "Gerenciar Usuários",
            "Gerenciar Livros",
            "Gerenciar Exemplares",
            "Gerenciar Empréstimos",
            "Gerenciar Solicitações",
            "Avaliar Usuário",
            "Ver Histórico"
        ]
        
        return View.exibir_menu(opcoes)


class UsuarioView(View):
    
    @staticmethod
    def menu_usuario():
        View.exibir_titulo("Gerenciar Usuários")
        
        opcoes = [
            "Criar novo usuário",
            "Listar usuários",
            "Buscar usuário",
            "Atualizar usuário",
            "Excluir usuário"
        ]
        
        return View.exibir_menu(opcoes)
    
    @staticmethod
    def formulario_usuario(editando=False):
        View.exibir_secao("Formulário de Usuário" if not editando else "Atualizar Usuário")
        
        username = input("Username: ")
        email = input("Email: ")
        idade = View.input_com_validacao("Idade", int)
        senha = input("Senha: ")
        
        return {
            "username": username,
            "email": email,
            "idade": idade,
            "senha": senha
        }
    
    @staticmethod
    def exibir_usuarios(usuarios):
        View.exibir_secao("Usuários Registrados")
        
        if not usuarios:
            View.exibir_aviso("Nenhum usuário registrado")
            return
        
        print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Idade':<5}")
        print("-" * 55)
        
        for usuario in usuarios:
            id_u, username, senha, idade, email = usuario
            print(f"{id_u:<5} {username:<15} {email:<25} {idade:<5}")


class LivroView(View):
    
    @staticmethod
    def menu_livro():
        View.exibir_titulo("Gerenciar Livros")
        
        opcoes = [
            "Adicionar novo livro",
            "Listar livros",
            "Buscar livro",
            "Atualizar livro",
            "Excluir livro"
        ]
        
        return View.exibir_menu(opcoes)
    
    @staticmethod
    def formulario_livro():
        View.exibir_secao("Formulário de Livro")
        
        titulo = input("Título: ")
        autor = input("Autor: ")
        paginas = View.input_com_validacao("Número de páginas", int)
        capa = input("URL da capa (opcional): ")
        
        return {
            "titulo": titulo,
            "autor": autor,
            "paginas": paginas,
            "capa": capa if capa else None
        }
    
    @staticmethod
    def exibir_livros(livros):
        View.exibir_secao("Livros Registrados")
        
        if not livros:
            View.exibir_aviso("Nenhum livro registrado")
            return
        
        print(f"{'ID':<5} {'Título':<25} {'Autor':<20} {'Páginas':<8}")
        print("-" * 60)
        
        for livro in livros:
            id_l, titulo, autor, paginas, capa = livro
            print(f"{id_l:<5} {titulo:<25} {autor:<20} {paginas:<8}")


class EmprestimoView(View):
    
    @staticmethod
    def menu_emprestimo():
        View.exibir_titulo("Gerenciar Empréstimos")
        
        opcoes = [
            "Criar novo empréstimo",
            "Listar empréstimos",
            "Marcar como devolvido",
            "Ver empréstimos ativos"
        ]
        
        return View.exibir_menu(opcoes)
    
    @staticmethod
    def exibir_emprestimos(emprestimos):
        View.exibir_secao("Empréstimos Registrados")
        
        if not emprestimos:
            View.exibir_aviso("Nenhum empréstimo registrado")
            return
        
        print(f"{'ID':<5} {'Exemplar':<10} {'Data Início':<15} {'Data Prevista':<15} {'Status':<10}")
        print("-" * 60)
        
        for emp in emprestimos:
            status = "Ativo" if emp[6] is None else "Devolvido"
            print(f"{emp[0]:<5} {emp[1]:<10} {emp[4]:<15} {emp[5]:<15} {status:<10}")


class AvaliacaoView(View):
    
    @staticmethod
    def formulario_avaliacao():
        View.exibir_secao("Avaliar Usuário")
        
        id_avaliado = View.input_com_validacao("ID do usuário a avaliar", int)
        nota = View.input_com_validacao("Nota (1-5)", int)
        comentario = input("Comentário (opcional): ")
        
        return {
            "id_avaliado": id_avaliado,
            "nota": nota,
            "comentario": comentario
        }
    
    @staticmethod
    def exibir_avaliacoes(avaliacoes):
        View.exibir_secao("Avaliações")
        
        if not avaliacoes:
            View.exibir_aviso("Nenhuma avaliação registrada")
            return
        
        print(f"{'ID':<5} {'Avaliador':<10} {'Avaliado':<10} {'Nota':<5} {'Comentário':<20}")
        print("-" * 55)
        
        for aval in avaliacoes:
            print(f"{aval[0]:<5} {aval[1]:<10} {aval[2]:<10} {aval[3]:<5} {aval[4][:20]:<20}")
