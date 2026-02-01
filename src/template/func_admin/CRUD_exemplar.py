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