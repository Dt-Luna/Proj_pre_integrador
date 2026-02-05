import streamlit as st
from views import Views
from datetime import datetime   
import pandas as pd
from pandas import DataFrame

class CRUD_usuario:
    def main():
        st.title("Usuários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Usuários", "Adicionar Usuário", "Atualizar Usuário", "Excluir Usuário"])
        with tab1: CRUD_usuario.listar_usuarios()
        with tab2: CRUD_usuario.adicionar_usuario()          
        with tab3: CRUD_usuario.atualizar_usuario() 
        with tab4: CRUD_usuario.excluir_usuario()

    def listar_usuarios():
        st.header("Listar Usuários")
        try:
            usuarios = Views.usuario_listar()
            if usuarios:
                df = DataFrame(usuarios, columns=["ID Usuário", "Nome", "Email", "Data de Nascimento"])
                st.dataframe(df)
            else:
                st.info("Nenhum usuário encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar usuários: {e}")
    
    def adicionar_usuario():
        st.header("Adicionar Usuário")
        nome = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")
        email = st.text_input("Email")
        data_nascimento = st.text_input("Data de Nascimento (AAAA-MM-DD)")

        if st.button("Adicionar Usuário"):
            try:
                Views.usuario_inserir(nome, senha, email, data_nascimento)
                st.success("Usuário adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar usuário: {e}")
        
    def atualizar_usuario():
        st.header("Atualizar Usuário")
        id = st.text_input("ID do Usuário a ser Atualizado")
        nome = st.text_input("Novo Nome")
        senha = st.text_input("Nova Senha", type="password")
        email = st.text_input("Novo Email")
        data_nascimento = st.text_input("Nova Data de Nascimento (AAAA-MM-DD)")

        if st.button("Atualizar Usuário"):
            try:
                Views.usuario_atualizar(id, nome, senha, email, data_nascimento)
                st.success("Usuário atualizado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao atualizar usuário: {e}")

    def excluir_usuario():
        st.header("Excluir Usuário")
        usuarios = Views.usuario_listar()
        op = st.selectbox("Selecione o usuário a ser excluído", usuarios)

        if st.button("Excluir Usuário"):
            try:
                id = op[0]
                Views.usuario_excluir(id)
                st.success("Usuário excluído com sucesso!")
            except Exception as e:
                st.error(f"Erro ao excluir usuário: {e}")