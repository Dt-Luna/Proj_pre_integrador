import streamlit as st
from views import Views
from datetime import datetime

class PerfilUI:
    def main():
        if 'usuario_logado' not in st.session_state:
            st.error("Você precisa estar logado para acessar o perfil.")
            return

        usuario = st.session_state['usuario_logado']
        st.title("Meus Dados")
        # com json
        '''op = View.cliente_listar_id(st.session_state["usuario_id"])
        nome = st.text_input("Informe o novo nome", op.get_nome())
        email = st.text_input("Informe o novo e-mail", op.get_email())
        fone = st.text_input("Informe o novo fone", op.get_fone())
        senha = st.text_input("Informe a nova senha", op.get_senha(),type="password")'''
        nome = st.text_input("Informe o novo nome", usuario['username'])
        email = st.text_input("Informe o novo e-mail", usuario['email'])
        senha = st.text_input("Informe a nova senha", type="password")
        data_nascimento = st.date_input("Informe a nova data de nascimento", usuario.get('data_nascimento'))
        if st.button("Atualizar"):
            try:
                Views.usuario_atualizar(usuario['id'], nome, senha, email, data_nascimento.strftime("%Y-%m-%d"))
                st.success("Dados atualizados com sucesso!")
                # Atualiza os dados na sessão
                st.session_state['usuario_logado']['username'] = nome
                st.session_state['usuario_logado']['email'] = email
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao atualizar dados: {e}")


        if st.button("Sair"):
            del st.session_state['usuario_logado']
            st.success("Você saiu com sucesso.")
            st.rerun()