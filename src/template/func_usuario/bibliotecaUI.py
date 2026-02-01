import streamlit as st
from views import Views
import pandas as pd
import time

class BibliotecaUI:
    def main():
        st.title("Biblioteca")
        tab1, tab2 = st.tabs(["Meus Exemplares", "Adicionar exemplar"])
        with tab1: BibliotecaUI.Ver()
        with tab2: BibliotecaUI.Adicionar()

    def Ver():
        user_exemplares = Views.exemplar_listar_por_usuario(st.session_state["usuario_id"])
        if len(user_exemplares) == 0: st.write("Você não tem exemplares cadastrados")
        else:
            list_dic = []

            for obj in user_exemplares: list_dic.append(obj.to_df())
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

    def Adicionar():
        livros = Views.livro_listar()      
        if len(livros) == 0: st.write("Não há livro modelo cadastrado")
        else:
            op = st.selectbox("Selecione o livro modelo: ", livros)
            if st.button("Inserir a biblioteca"):

                Views.exemplar_inserir(st.session_state["usuario_id"], op)
                st.success(f"Exemplar de {op.get_titulo()} inserido na sua biblioteca com sucesso!")
                time.sleep(2)
                st.rerun()