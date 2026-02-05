import streamlit as st
from views import Views
import time

class LoginUI:
    def main():
        st.header("Entrar no Sistema")
        
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        
        if st.button("Entrar"):
            #try:
            # A View agora retorna um DICIONÁRIO: {'id': 1, 'username': '...', ...}
            usuario = Views.usuario_autenticar(email, senha)

            if usuario:
                user_id = usuario['id']
                user_nome = usuario['username']
                user_email = usuario['email']
                user_senha = usuario['senha']
                user_data_nascimento = usuario['data_nascimento']

                st.success(f"Bem-vindo(a), {user_nome}!")
                
                st.session_state["usuario_id"] = user_id
                st.session_state["usuario_nome"] = user_nome
                st.session_state["usuario_email"] = user_email
                st.session_state["usuario_senha"] = user_senha
                st.session_state["usuario_data_nascimento"] = user_data_nascimento
                st.session_state["usuario_logado"] = True 

                time.sleep(1) 
                st.rerun()    
            else:
                st.error("E-mail ou senha inválidos.")
        
        # except Exception as e:
            # Dica: Se der erro de novo, imprima o tipo do erro para facilitar
            #st.error(f"Ocorreu um erro no login: {type(e).__name__} - {e}")