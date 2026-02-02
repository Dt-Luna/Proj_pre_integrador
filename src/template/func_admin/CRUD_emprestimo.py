import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd
import time

class CRUD_emprestimo:
    def main():
        st.title("Empréstimos")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Empréstimos", "Adicionar Empréstimo", "Atualizar Empréstimo", "Excluir Empréstimo"])
        with tab1: CRUD_emprestimo.listar_emprestimos()
        # with tab2: CRUD_emprestimo.adicionar_emprestimo()          
        # with tab3: CRUD_emprestimo.atualizar_emprestimo()
        # with tab4: CRUD_emprestimo.excluir_emprestimo()
        
    def listar_emprestimos():
        st.header("Listar Empréstimos")
        try:
            emprestimos = Views.emprestimo_listar()
            if emprestimos:
                df = pd.DataFrame(emprestimos)
                st.dataframe(df)
            else:
                st.info("Nenhum empréstimo encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar empréstimos: {e}")