import streamlit as st
from views import Views
import time

class LoginUI:
    def main():
        st.header("Entrar no Sistema")
        
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Entrar"):
            try:
                # O DAO retorna uma tupla: (id, username, senha, nascimento, email)
                usuario = Views.usuario_autenticar(email, senha)

                if usuario:
                    # CORREÇÃO: Acessando por índice (posição na tabela)
                    # 0=id, 1=username, 2=senha, 3=nascimento, 4=email
                    
                    user_id = usuario[0]
                    user_nome = usuario[1]
                    user_email = usuario[4]

                    st.success(f"Bem-vindo(a), {user_nome}!")
                    
                    # Salvando na sessão para o index.py usar
                    st.session_state["usuario_id"] = user_id
                    st.session_state["usuario_nome"] = user_nome
                    st.session_state["usuario_email"] = user_email
                    
                    # Guarda um flag extra para facilitar verificações futuras
                    st.session_state["usuario_logado"] = True

                    time.sleep(1) 
                    st.rerun()    
                else:
                    st.error("E-mail ou senha inválidos.")
            
            except Exception as e:
                st.error(f"Ocorreu um erro no login: {e}")