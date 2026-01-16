import streamlit as st
from views import View
import time

class AbrirContaUI:
    def main():
        st.title("Abrir Conta no Sistema")
        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        idade = st.number_input("Informe sua idade")
        
        if st.button("Inserir"):
            '''
                    Excessões
            '''

            View.cliente_inserir(nome, senha, email, idade)
            st.success("Conta criada com sucesso!")
            time.sleep(2)
            st.rerun()

        '''usuario = Usuario(None, "joao_silva", "senha123", "joao@email.com", 25)
        id_usuario = dao_usuario.inserir(usuario)
        print(f"  ✓ Usuário inserido com ID: {id_usuario}")'''