import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd

class PesquisarUI:
    def main():
        st.title("Pesquisar")
        
        livros = Views.livro_listar()
        termos = st.text_input("Digite o termo de pesquisa (título, autor, gênero):")
        resultados = [livro for livro in livros if termos.lower() in livro[1].lower() 
                      or termos.lower() in livro[2].lower() 
                      or termos.lower() in livro[3].lower()]
        df = pd.DataFrame(resultados)
        st.dataframe(df)