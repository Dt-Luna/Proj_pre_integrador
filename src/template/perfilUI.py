import streamlit as st
from views import Views
import time

class PerfilUI:
    def main():
        st.header("Perfil do Usuário")

        id_usuario = st.session_state.get("usuario_id")
        username_atual = st.session_state.get("usuario_nome")
        email_atual = st.session_state.get("usuario_email")
        data_nascimento_atual = st.session_state.get("usuario_data_nascimento")
        senha_atual = st.session_state.get("usuario_senha")

        if not id_usuario:
            st.error("Nenhum usuário logado.")
            return

        novo_nome = st.text_input("Nome de usuário", value=username_atual)
        novo_email = st.text_input("E-mail", value=email_atual)
        nova_senha = st.text_input("Nova Senha", type="password", value=senha_atual)
        data_nascimento = st.text_input("Data de Nascimento (AAAA-MM-DD)", value=data_nascimento_atual) 

        if st.button("Atualizar Perfil"):
          #try:
            # Chama a View para atualizar
            Views.usuario_atualizar(
                id_usuario, 
                novo_nome, 
                nova_senha, 
                novo_email, 
                data_nascimento
            )
            
            st.success("Perfil atualizado com sucesso!")
            
            st.session_state["usuario_nome"] = novo_nome
            st.session_state["usuario_email"] = novo_email
            
            time.sleep(2)
            st.rerun()
            
        # except Exception as e:
            st.error(f"Erro ao atualizar perfil: {e}")