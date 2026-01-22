import streamlit as st
from views import Views
import time
from datetime import date

class CriarContaUI:
    def main():
        st.info("Já possui uma conta? Vá para a tela de login.")
        st.title("Abrir Conta no Sistema")
        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        data_nascimento = st.date_input("Informe a data de nascimento", min_value=date(1925, 1, 1), max_value=date.today())
        
        if st.button("Inserir"):
            try:
                Views.usuario_inserir(nome, senha, email, data_nascimento.strftime("%Y-%m-%d"))
                st.success("Conta criada com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao criar conta: {e}")
            time.sleep(2)
            st.rerun()
