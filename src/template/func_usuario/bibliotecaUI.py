import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd
import time

class BibliotecaUI:
    def main():
        st.title("Biblioteca")
        st.write("Bem-vindo à Biblioteca!")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Exemplares", "Adicionar Exemplar", "Atualizar Exemplar", "Excluir Exemplar"])
        with tab1: BibliotecaUI.listar_exemplares()
        with tab2: BibliotecaUI.adicionar_exemplar()           
        # with tab3: BibliotecaUI.atualizar_exemplar()
        with tab4: BibliotecaUI.excluir_exemplar()
    def listar_exemplares():   
        st.header("Listar Exemplares")
        try:
            exemplares = Views.exemplar_listar()
            if exemplares:
                df = pd.DataFrame(exemplares)
                st.dataframe(df)
            else:
                st.info("Nenhum exemplar encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar exemplares: {e}")

    def adicionar_exemplar():
        livros = Views.livro_listar()
        if livros:
            id_usuario = st.session_state.get("usuario_id")
            id_livro = st.selectbox('Escolha um livro', livros)
            if st.button('Inserir'):
                Views.exemplar_inserir(id_usuario, id_livro)
        else:
            st.write('Nenhum livro encontrado')

    # def atualizar_exemplar():
        # exemplares = Views.exemplar_listar_por_usuario(st.session_state.get('usuario_id'))
        # livros = Views.livro_listar()
        # if exemplares:
        #     op = st.selectbox('Selecione o exemplar', exemplares)
        #     livro = st.selectbox('Selecione o livro', livros)
        #     if st.button('Atualizar'):
        #         try:
        #             Views.exemplar_atualizar(op[0], st.session_state.get('usuario_id'), livro)
        # else:
        #     st.write('Nenhum exemplar cadastrado')

    def excluir_exemplar():
        exemplares = Views.exemplar_listar()
        if exemplares:
            op = st.selectbox('Selecione o exemplar',  exemplares)
            if st.button('Excluir'):
                try:
                    Views.exemplar_excluir(op[0])
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f'Erro ao excluir exemplar: {e}')

    