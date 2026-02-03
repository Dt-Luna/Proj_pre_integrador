import streamlit as st
from views import Views
import pandas as pd
import time

class DevolucoesUI:
    def main():
        st.title("Devoluções")
        tab1, tab2 = st.tabs(["Minhas Devoluções", "Confirmar Devoluções"])
        with tab1: DevolucoesUI.minhas_devolucoes()
        with tab2: DevolucoesUI.confirmar_devolucoes()

    def minhas_devolucoes():
        st.header("Solicitar Devolução")
        
        try:
            # Listar empréstimos ativos do usuário
            emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
            emprestimos_ativos = [e for e in emprestimos if e[4] is None]  # data_devolucao is None
            
            if not emprestimos_ativos:
                st.info("Você não tem empréstimos ativos para devolver.")
                return
            
            # Exibir empréstimos ativos
            for emprestimo in emprestimos_ativos:
                id_emprestimo = emprestimo[0]
                id_solicitacao = emprestimo[1]
                data_inicio = emprestimo[2]
                data_prevista = emprestimo[3]
                
                # Obter detalhes da solicitação e exemplar
                solicitacao = Views.solicitacao_listar_id(id_solicitacao)
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Livro:** {livro[1]}")
                        st.markdown(f"**Autor:** {livro[2]}")
                        st.markdown(f"**Início:** {data_inicio}")
                        st.markdown(f"**Previsão:** {data_prevista}")
                    
                    with col2:
                        if st.button("Devolver", key=f"devolver_{id_emprestimo}"):
                            try:
                                Views.solicitar_devolucao(id_emprestimo)
                                st.success("Devolução solicitada com sucesso! Aguarde confirmação do dono.")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao solicitar devolução: {str(e)}")
                
        except Exception as e:
            st.error(f"Erro ao carregar devoluções: {str(e)}")

    def confirmar_devolucoes():
        st.header("Confirmar Devoluções Recebidas")
        
        try:
            # Listar devoluções pendentes para o dono
            devolucoes_pendentes = Views.listar_devolucoes_pendentes_por_dono(st.session_state["usuario_id"])
            
            if not devolucoes_pendentes:
                st.info("Você não tem devoluções pendentes para confirmar.")
                return
            
            # Exibir devoluções pendentes
            for devolucao in devolucoes_pendentes:
                id_emprestimo = devolucao[0]
                id_solicitacao = devolucao[1]
                data_inicio = devolucao[2]
                data_prevista = devolucao[3]
                data_devolucao = devolucao[4]
                
                # Obter detalhes
                solicitacao = Views.solicitacao_listar_id(id_solicitacao)
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                solicitante = Views.usuario_listar_por_id(solicitacao[5])
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Livro:** {livro[1]}")
                        st.markdown(f"**Solicitante:** {solicitante[1]}")
                        st.markdown(f"**Data Devolução:** {data_devolucao}")
                    
                    with col2:
                        if st.button("Confirmar", key=f"confirmar_{id_emprestimo}"):
                            try:
                                Views.confirmar_devolucao(id_emprestimo)
                                st.success("Devolução confirmada com sucesso! Exemplar disponível novamente.")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao confirmar devolução: {str(e)}")
                
        except Exception as e:
            st.error(f"Erro ao carregar devoluções pendentes: {str(e)}")
