import streamlit as st
from views import Views
from datetime import datetime

class CRUD_exemplar:
    def main():
        st.title("Exemplares")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Exemplares", "Adicionar Exemplar", "Atualizar Exemplar", "Excluir Exemplar"])
        with tab1: CRUD_exemplar.listar_exemplares()
        with tab2: CRUD_exemplar.adicionar_exemplar()           
        with tab3: CRUD_exemplar.atualizar_exemplar()
        with tab4: CRUD_exemplar.excluir_exemplar()
    
    def listar_exemplares():   
        st.header("Listar Exemplares")
        try:
            exemplares = Views.exemplar_listar()
            if exemplares:
                for ex in exemplares:
                    st.write(f"ID Exemplar: {ex[0]}, ID Usuário: {ex[1]}, ID Livro: {ex[2]}, Status: {ex[3]}")
            else:
                st.info("Nenhum exemplar encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar exemplares: {e}")
    
    def adicionar_exemplar():
        st.header("Adicionar Exemplar")
        with st.form("form_adicionar_exemplar"):
            id_usuario = st.number_input("ID do Usuário", min_value=1, value=1)
            id_livro = st.number_input("ID do Livro", min_value=1, value=1)
            submit_button = st.form_submit_button("Adicionar Exemplar")
            
            if submit_button:
                try:
                    Views.exemplar_inserir(id_usuario, id_livro)
                    st.success("Exemplar adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar exemplar: {e}")
    
    def atualizar_exemplar():
        st.header("Atualizar Exemplar")
        with st.form("form_atualizar_exemplar"):
            id_exemplar = st.number_input("ID do Exemplar", min_value=1, value=1)
            id_usuario = st.number_input("ID do Usuário", min_value=1, value=1)
            id_livro = st.number_input("ID do Livro", min_value=1, value=1)
            status = st.selectbox("Status", ["disponivel", "emprestado", "manutencao"])
            submit_button = st.form_submit_button("Atualizar Exemplar")
            
            if submit_button:
                try:
                    Views.exemplar_atualizar(id_exemplar, id_usuario, id_livro, status)
                    st.success("Exemplar atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar exemplar: {e}")
    
    def excluir_exemplar():
        st.header("Excluir Exemplar")
        with st.form("form_excluir_exemplar"):
            id_exemplar = st.number_input("ID do Exemplar para Excluir", min_value=1, value=1)
            submit_button = st.form_submit_button("Excluir Exemplar")
            
            if submit_button:
                try:
                    Views.exemplar_excluir(id_exemplar)
                    st.success("Exemplar excluído com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir exemplar: {e}")