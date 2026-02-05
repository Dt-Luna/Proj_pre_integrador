import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd
import time

class CRUD_livro:
    def main():
        st.title("Livros")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Livros", "Adicionar Livro", "Atualizar Livro", "Excluir Livro"])
        with tab1: CRUD_livro.listar_livros()
        with tab2: CRUD_livro.adicionar_livro()
        with tab3: CRUD_livro.atualizar_livro()
        with tab4: CRUD_livro.excluir_livro()


    def listar_livros():
        st.header("Listar Livros")
        try:
            livros = Views.livro_listar()
            if livros:
                df = pd.DataFrame(livros)
                st.dataframe(df)
            else:
                st.info("Nenhum livro encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar livros: {e}")

    def adicionar_livro():
        st.header('adicionar livros')
        titulo = st.text_input('Título do livro')
        autor = st.text_input('Autor do livro')
        paginas = st.number_input('Páginas do livro')
        isbn = st.text_input('Isbn do livro')

        if st.button('Inserir'):
            try:
                Views.livro_inserir(titulo, autor, paginas, isbn)
                st.success('Livro inserido com sucesso')
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f'Erro ao adicionar livro: {e}')
    
    def atualizar_livro():
        livros = Views.livro_listar()
        if not livros: st.write('Nenhum livro cadastrado')
        else:
            op = st.selectbox('Escolha o livro', livros, key='update_exemplar')
            titulo = st.text_input('Novo título', key='update_titulo')
            autor = st.text_input('Autor do livro', key='update_autor')
            paginas = st.number_input('Páginas do livro', key='update_paginas')
            isbn = st.text_input('ISBN', key='update_isbn')
            if st.button('Atualizar'):
                try:
                    Views.livro_atualizar(op[0], titulo, autor, paginas, isbn)
                    st.success('Livro atualizado com sucesso')
                except Exception as e:
                    st.error(f'Erro ao atualizar livro: {e}')
    
    def excluir_livro():
        livros = Views.livro_listar()
        if not livros: st.write('Nenhum livro cadastrado')
        else:
            op = st.selectbox('Escolha o livro', livros)
            if st.button('Excluir'):
                try:
                    Views.livro_excluir(op[0])
                    st.success('Livro excluído com sucesso')
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f'Erro ao excluir livro: {e}')