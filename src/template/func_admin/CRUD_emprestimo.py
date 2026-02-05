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
        with tab2: CRUD_emprestimo.adicionar_emprestimo()          
        with tab3: CRUD_emprestimo.atualizar_emprestimo()
        with tab4: CRUD_emprestimo.excluir_emprestimo()

    def listar_emprestimos():
        st.header("Listar Empréstimos")
        try:
            emprestimos = Views.emprestimo_listar()
            if emprestimos:
                df = pd.DataFrame(emprestimos, columns=[
                    "ID", "ID Solicitação", "Data Início", "Data Prevista", "Data Devolução"
                ])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum empréstimo encontrado.")
        except Exception as e:
            st.error(f"Erro ao listar empréstimos: {e}")

    def adicionar_emprestimo():
        st.header("Adicionar Empréstimo")
        
        solicitacoes = Views.solicitacao_listar()
        solicitacoes_aceitas = [s for s in solicitacoes if s[2] == "aceita"]
        
        emprestimos_existentes = Views.emprestimo_listar()
        ids_solicitacoes_usadas = [e[1] for e in emprestimos_existentes if len(e) > 1]
        
        solicitacoes_disponiveis = [
            s for s in solicitacoes_aceitas 
            if s[0] not in ids_solicitacoes_usadas
        ]
        
        if not solicitacoes_disponiveis:
            st.info("Não há solicitações aceitas disponíveis para criar empréstimos.")
            return
        
        with st.form("form_adicionar_emprestimo"):
            opcoes_solicitacao = {}
            for solicitacao in solicitacoes_disponiveis:
                solicitacao_id = solicitacao[0]
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                solicitante = Views.usuario_listar_por_id(solicitacao[5])
                opcoes_solicitacao[solicitacao_id] = f"ID {solicitacao_id} - {livro[1]} (Solicitante: {solicitante[1]})"
            
            selected_solicitacao_id = st.selectbox(
                "Selecione a Solicitação:",
                options=list(opcoes_solicitacao.keys()),
                format_func=lambda x: opcoes_solicitacao[x]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input("Data de Início:", value=datetime.now().date())
            with col2:
                data_prevista = st.date_input(
                    "Data Prevista para Devolução:", 
                    value=datetime.now().date() + pd.Timedelta(days=7)
                )
            
            submit_button = st.form_submit_button("Adicionar Empréstimo")
            
            if submit_button:
                try:
                    if data_inicio > data_prevista:
                        st.error("Data de início não pode ser posterior à data prevista!")
                        return
                    
                    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
                    data_prevista_str = data_prevista.strftime("%Y-%m-%d")
                    
                    Views.emprestimo_inserir(
                        selected_solicitacao_id, 
                        data_inicio_str, 
                        data_prevista_str
                    )
                    
                    st.success("Empréstimo adicionado com sucesso!")
                    time.sleep(2)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro ao adicionar empréstimo: {str(e)}")

    def atualizar_emprestimo():
        st.header("Atualizar Empréstimo")
        
        emprestimos = Views.emprestimo_listar()
        
        if not emprestimos:
            st.info("Nenhum empréstimo encontrado para atualizar.")
            return
        
        with st.form("form_atualizar_emprestimo"):
            opcoes_emprestimo = {}
            for emprestimo in emprestimos:
                if len(emprestimo) > 1:
                    emprestimo_id = emprestimo[0]
                    solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                    if solicitacao:
                        exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                        if exemplar:
                            livro = Views.livro_listar_por_id(exemplar[2])
                            opcoes_emprestimo[emprestimo_id] = f"ID {emprestimo_id} - {livro[1]}"
            
            selected_emprestimo_id = st.selectbox(
                "Selecione o Empréstimo:",
                options=list(opcoes_emprestimo.keys()),
                format_func=lambda x: opcoes_emprestimo[x]
            )
            
            emprestimo_detalhes = Views.emprestimo_listar_id(selected_emprestimo_id)
            
            if emprestimo_detalhes and len(emprestimo_detalhes) > 1:
                col1, col2 = st.columns(2)
                with col1:
                    data_inicio = st.date_input(
                        "Data de Início:", 
                        value=pd.to_datetime(emprestimo_detalhes[2]).date() if emprestimo_detalhes[2] else datetime.now().date()
                    )
                with col2:
                    data_prevista = st.date_input(
                        "Data Prevista para Devolução:", 
                        value=pd.to_datetime(emprestimo_detalhes[3]).date() if emprestimo_detalhes[3] else datetime.now().date()
                    )
                
                data_devolucao = st.date_input(
                    "Data de Devolução (opcional):", 
                    value=pd.to_datetime(emprestimo_detalhes[4]).date() if emprestimo_detalhes[4] else None
                )
                
                submit_button = st.form_submit_button("Atualizar Empréstimo")
                
                if submit_button:
                    try:
                        if data_inicio > data_prevista:
                            st.error("Data de início não pode ser posterior à data prevista!")
                            return
                        
                        data_inicio_str = data_inicio.strftime("%Y-%m-%d")
                        data_prevista_str = data_prevista.strftime("%Y-%m-%d")
                        data_devolucao_str = data_devolucao.strftime("%Y-%m-%d") if data_devolucao else None
                        
                        Views.emprestimo_atualizar(
                            selected_emprestimo_id,
                            emprestimo_detalhes[1],
                            data_inicio_str, 
                            data_prevista_str,
                            data_devolucao_str
                        )
                        
                        st.success("Empréstimo atualizado com sucesso!")
                        time.sleep(2)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Erro ao atualizar empréstimo: {str(e)}")
            else:
                st.error("Empréstimo selecionado não encontrado!")

    def excluir_emprestimo():
        st.header("Excluir Empréstimo")
        
        emprestimos = Views.emprestimo_listar()
        
        if not emprestimos:
            st.info("Nenhum empréstimo encontrado para excluir.")
            return
        
        with st.form("form_excluir_emprestimo"):
            opcoes_emprestimo = {}
            for emprestimo in emprestimos:
                if len(emprestimo) > 1:
                    emprestimo_id = emprestimo[0]
                    solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                    if solicitacao:
                        exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                        if exemplar:
                            livro = Views.livro_listar_por_id(exemplar[2])
                            opcoes_emprestimo[emprestimo_id] = f"ID {emprestimo_id} - {livro[1]}"
            
            selected_emprestimo_id = st.selectbox(
                "Selecione o Empréstimo:",
                options=list(opcoes_emprestimo.keys()),
                format_func=lambda x: opcoes_emprestimo[x]
            )
            
            if selected_emprestimo_id:
                emprestimo_detalhes = Views.emprestimo_listar_id(selected_emprestimo_id)
                
                if emprestimo_detalhes and len(emprestimo_detalhes) > 1:
                    st.write("**Detalhes do Empréstimo:**")
                    
                    solicitacao = Views.solicitacao_listar_id(emprestimo_detalhes[1])
                    if solicitacao:
                        exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                        if exemplar:
                            livro = Views.livro_listar_por_id(exemplar[2])
                            solicitante = Views.usuario_listar_por_id(solicitacao[5])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Livro:** {livro[1]}")
                                st.write(f"**Solicitante:** {solicitante[1]}")
                                st.write(f"**Data Início:** {emprestimo_detalhes[2]}")
                            with col2:
                                st.write(f"**Data Prevista:** {emprestimo_detalhes[3]}")
                                st.write(f"**Data Devolução:** {emprestimo_detalhes[4] or 'Não devolvido'}")
                    
                    st.warning("Esta ação não pode ser desfeita!")
                    
                    submit_button = st.form_submit_button("Confirmar Exclusão")
                    
                    if submit_button:
                        try:
                            Views.emprestimo_excluir(selected_emprestimo_id)
                            st.success("Empréstimo excluído com sucesso!")
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao excluir empréstimo: {str(e)}")
                else:
                    st.error("Empréstimo selecionado não encontrado!")
