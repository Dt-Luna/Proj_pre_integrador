from template.adminUI import manterusuario, manterlivro
from template.usuarioUI import biblioteca, solicitacao, avaliar, pesquisa
from template.perfilUI import perfil
from template.criarcontaUI import criarconta
from template.loginUI import login
from views import Views
import streamlit as st

class IndexUI:

    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        #View.cliente_criar_admin()
        if op == "Entrar no Sistema": login.main()
        if op == "Abrir Conta": criarconta.main()

    def menu_cliente(): 
        op = st.sidebar.selectbox("Menu", ["Perfil", "Biblioteca", "Solicitações","Avaliar", "Pesquisa"])
        if op == "Perfil": perfil.main()
        if op == "Biblioteca": biblioteca.main()
        if op == "Solicitações": solicitacao.main()
        if op == "Avaliar": avaliar.main()
        if op == "Pesquisa": pesquisa.main()

    def menu_admin():            
        op = st.sidebar.selectbox("Menu", ["Perfil", "Usuários Comuns", "Modelo de Livro"])
        if op == "Perfil": perfil.main()
        if op == "Usuários Comuns": manterusuario.main()
        if op == "Modelo de Livro": manterlivro.main()

    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            admin = st.session_state["usuario_nome"] == "admin"

            st.sidebar.write("Bem-vindo(a), " + st.session_state["usuario_nome"])

            if admin: IndexUI.menu_admin()
            else: IndexUI.menu_usuario()
            IndexUI.sair()
    
    def sair():
        if st.sidebar.button("Logout"):
            del st.session_state["usuario_id"]
            del st.session_state["usuario_nome"]
            st.rerun()

IndexUI.sidebar()