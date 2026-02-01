from template.func_admin.CRUD_avalicao import CRUD_avalicao
from template.func_admin.CRUD_emprestimo import CRUD_emprestimo 
from template.func_admin.CRUD_exemplar import CRUD_exemplar
from template.func_admin.CRUD_livro import CRUD_livro
from template.func_admin.CRUD_usuario import CRUD_usuario
from template.func_usuario.bibliotecaUI import BibliotecaUI
from template.func_usuario.solicitacaoUI import SolicitacaoUI
from template.func_usuario.avaliarUI import AvaliarUI
from template.func_usuario.pesquisarUI import PesquisarUI    
from template.perfilUI import PerfilUI
from template.criarcontaUI import CriarContaUI
from template.loginUI import LoginUI
from views import Views
from dao.database import Database
import streamlit as st

class IndexUI:

    @staticmethod
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir Conta": CriarContaUI.main()

    @staticmethod
    def menu_cliente(): 
        op = st.sidebar.selectbox("Menu", ["Perfil", "Biblioteca", "Solicitações", "Avaliar", "Pesquisa"])
        if op == "Perfil": PerfilUI.main()
        if op == "Biblioteca": BibliotecaUI.main()
        if op == "Solicitações": SolicitacaoUI.main()
        if op == "Avaliar": AvaliarUI.main()
        if op == "Pesquisa": PesquisarUI.main()

    @staticmethod
    def menu_admin():            
        # CORREÇÃO 1: Adicionadas todas as opções na lista
        op = st.sidebar.selectbox("Menu", ["Perfil", "Usuários Comuns", "Modelo de Livro", "Avaliações", "Empréstimos", "Exemplares"])
        
        if op == "Perfil": PerfilUI.main()
        if op == "Usuários Comuns": CRUD_usuario.main()
        if op == "Modelo de Livro": CRUD_livro.main()
        if op == "Avaliações": CRUD_avalicao.main()
        if op == "Empréstimos": CRUD_emprestimo.main()
        if op == "Exemplares": CRUD_exemplar.main()

    @staticmethod
    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            # CORREÇÃO 2: Verificando pelo perfil (ideal) ou email, não apenas pelo nome
            # Nota: O ideal é salvar 'usuario_perfil' no session_state durante o login.
            # Por enquanto, vou supor que o admin é quem tem o ID 1 ou o nome exato do banco.
            
            # Ajuste aqui conforme o que você salvou no LoginUI.
            # Se no login você salvou o email, use: st.session_state["usuario_email"] == "admin@sistema.com"
            is_admin = False
            
            # Verificação provisória (ajuste conforme seu LoginUI):
            if st.session_state.get("usuario_email") == "admin@sistema.com": # Email exato do admin no banco
                is_admin = True
            
            # Se você tiver salvo o perfil no login, seria melhor:
            # if st.session_state.get("usuario_perfil") == "admin": is_admin = True

            st.sidebar.write("Bem-vindo(a), " + st.session_state["usuario_nome"])

            if is_admin: 
                IndexUI.menu_admin()
            else: 
                IndexUI.menu_cliente() # CORREÇÃO 3: Nome do método corrigido (era menu_usuario)
            
            IndexUI.sair()
    
    @staticmethod
    def sair():
        if st.sidebar.button("Logout"):
            if "usuario_id" in st.session_state: del st.session_state["usuario_id"]
            if "usuario_nome" in st.session_state: del st.session_state["usuario_nome"]
            if "usuario_email" in st.session_state: del st.session_state["usuario_email"]
            st.rerun()

    @staticmethod
    def main():
        try:
            db = Database() # Isso roda o __init__ que chama criar_tabelas()
            db.fechar()     # Fecha conexão, pois o DAO abrirá a sua própria depois
        except Exception as e:
            st.error(f"Erro fatal ao iniciar banco de dados: {e}")
            return
        # Verifica e cria o admin se não existir
        Views.criar_admin()
        IndexUI.sidebar()

if __name__ == "__main__":
    IndexUI.main()