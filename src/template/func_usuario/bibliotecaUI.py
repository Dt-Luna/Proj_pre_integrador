import streamlit as st
from views import Views
import pandas as pd
import time

class BibliotecaUI:
    def main():
        st.title("Biblioteca")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Exemplares", "Adicionar exemplar", "Atualizar Exemplar", "Excluir Exemplar"])
        with tab1: BibliotecaUI.Ver()
        with tab2: BibliotecaUI.Adicionar()
        with tab3: BibliotecaUI.atualizar_exemplar()
        with tab4: BibliotecaUI.excluir_exemplar()

    def Ver():
        #st.header("Listar Exemplares")
        try:
            user_exemplares = Views.exemplar_listar_por_usuario(st.session_state.get("usuario_id"))
            if len(user_exemplares) == 0: st.write("Você não tem exemplares cadastrados")
            else:
                df = pd.DataFrame(user_exemplares)               
                st.dataframe(df)

        except Exception as e:
            st.error(f"Erro ao listar exemplares: {e}")

    def Adicionar():
        livros = Views.livro_listar()      
        if livros: 
            id_usuario = st.session_state.get("usuario_id")
            op = st.selectbox("Selecione o livro modelo: ", livros)

            if st.button("Inserir a biblioteca"):
                Views.exemplar_inserir(id_usuario, op[0])
                st.success(f"Exemplar de inserido na sua biblioteca com sucesso!")
                time.sleep(2)
                st.rerun()
        else:
            st.write("Nenhum livro modelo cadastrado")

    def atualizar_exemplar():
        exemplares = Views.exemplar_listar_por_usuario(st.session_state.get('usuario_id'))
        livros = Views.livro_listar()
        if exemplares:
            op = st.selectbox('Selecione o exemplar', exemplares)
            status_op = st.selectbox('Selecione o status', ['disponivel', 'emprestado', 'indisponivel'])
            if st.button('Atualizar'):
                try:
                    Views.exemplar_atualizar(op[0], op[1], op[2], status_op)
                    st.success("Exemplar atualizado com sucesso!")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f'Erro ao atualizar exemplar: {e}')
        else:
            st.write('Nenhum exemplar cadastrado')

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