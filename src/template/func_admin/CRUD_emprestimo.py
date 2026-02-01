import streamlit as st
from views import Views
from datetime import datetime

class CRUD_emprestimo:
    def main():
        st.title("Empréstimos")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Empréstimos", "Adicionar Empréstimo", "Atualizar Empréstimo", "Excluir Empréstimo"])
        with tab1: CRUD_emprestimo.listar_emprestimos()
        with tab2: CRUD_emprestimo.adicionar_emprestimo()           
        with tab3: CRUD_emprestimo.atualizar_emprestimo()
        with tab4: CRUD_emprestimo.excluir_emprestimo()
    def listar_emprestimos():
        st.header("Listar Empréstimos")
        try:
            emprestimos = Views.emprestimo_listar()
            if emprestimos:
                for emp in emprestimos:
                    st.write(f"ID Empréstimo: {emp[0]}, ID Solicitação: {emp[1]}, Data Início: {emp[2]}, Data Prevista: {emp[3]}, Data Devolução: {emp[4]}")
            else:
                st.info("Nenhum empréstimo encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar empréstimos: {e}")