import streamlit as st
from views import Views
from datetime import datetime, date, timedelta
import pandas as pd
import time

class SolicitacaoUI:
    def main():
        st.title("Gerenciamento de Solicitações")
        
        # Separar em abas mais lógicas
        tab1, tab2, tab3 = st.tabs(["Minhas Solicitações", "✅ Avaliar Solicitações", "📚 Meus Empréstimos como Dono"])
        
        with tab1: SolicitacaoUI.Ver()
        with tab2: SolicitacaoUI.Avaliar()
        with tab3: SolicitacaoUI.EmprestimosComoDono()


    def Ver():
        user_solicitacoes = Views.solicitacao_listar_por_usuario(st.session_state["usuario_id"])
        if user_solicitacoes:
            data = []
            for obj in user_solicitacoes:
                data.append({
                    'ID': obj[0],
                    'Data': obj[1], 
                    'Status': obj[2],
                    'Dias': obj[3],
                    'Exemplar': obj[4],
                    'Solicitante': obj[5]
                })
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("Ainda não foi submetida solicitação de empréstimo")

    def Avaliar():
        st.subheader("Avaliar Solicitações de Empréstimo")
        st.write("Aqui você pode aprovar ou rejeitar solicitações para seus exemplares.")
        
        if "usuario_id" not in st.session_state:
            st.error("Você não está logado!")
            return
            
        usuario_id = st.session_state["usuario_id"]
        usuario_nome = st.session_state.get("usuario_nome", "Desconhecido")
        
        solicitacoes = Views.solicitacao_listar_pendentes_por_dono(usuario_id)
        
        if solicitacoes:
            st.success(f"Você tem {len(solicitacoes)} solicitação(ões) pendente(s):")
            
            for obj in solicitacoes:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        try:
                            exemplar_info = Views.exemplar_listar_por_id(obj[4])
                            if exemplar_info:
                                livro_info = Views.livro_listar_por_id(exemplar_info[2])
                                nome_livro = livro_info[1] if livro_info else "Livro desconhecido"
                                nome_exemplar = f"Exemplar {obj[4]} - {nome_livro}"
                            else:
                                nome_exemplar = f"Exemplar {obj[4]}"
                            
                            solicitante_info = Views.usuario_listar_por_id(obj[5])
                            nome_solicitante = solicitante_info[1] if solicitante_info else f"Usuário {obj[5]} (inativo)"
                            
                            st.markdown(f"**{nome_exemplar}**")
                            st.markdown(f"**Solicitante:** {nome_solicitante}")
                            st.markdown(f"**Data:** {obj[1]}")
                            st.markdown(f"**Dias solicitados:** {obj[3]}")
                            st.markdown(f"**Status:** {obj[2]}")
                            
                        except Exception as e:
                            st.error(f"Erro ao carregar detalhes: {e}")
                            st.write(f"Solicitação ID: {obj[0]}, Data: {obj[1]}, Status: {obj[2]}, Dias: {obj[3]}, Exemplar: {obj[4]}, Solicitante: {obj[5]}")
                    
                    with col2:
                        if st.button(f"Aprovar", key=f"aprovar_{obj[0]}", use_container_width=True):
                            try:
                                Views.aprovar_solicitacao(obj[0])
                                st.success("Solicitação aprovada com sucesso!")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao aprovar: {str(e)}")
                    
                    with col3:
                        if st.button(f"Rejeitar", key=f"rejeitar_{obj[0]}", use_container_width=True):
                            try:
                                Views.rejeitar_solicitacao(obj[0])
                                st.success("Solicitação rejeitada com sucesso!")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao rejeitar: {str(e)}")
        else:
            st.info("**Nenhuma solicitação pendente**")
            st.write("Quando outros usuários solicitarem seus exemplares, elas aparecerão aqui para aprovação.")
            
            try:
                meus_exemplares = Views.exemplar_listar_por_usuario(st.session_state["usuario_id"])
                if meus_exemplares:
                    st.write(f"**Seus exemplares disponíveis:** {len([ex for ex in meus_exemplares if ex[3] == 'disponivel'])}")
                    for ex in meus_exemplares:
                        if ex[3] == 'disponivel':
                            st.write(f"  • Exemplar {ex[0]} - Status: {ex[3]}")
                else:
                    st.write("Você não possui exemplares cadastrados.")
            except Exception as e:
                st.error(f"Erro ao verificar seus exemplares: {e}")

    def EmprestimosComoDono():
        st.subheader("Meus Empréstimos como Dono")
        st.write("Acompanhe os empréstimos ativos de seus exemplares.")
        
        if "usuario_id" not in st.session_state:
            st.error("Você não está logado!")
            return
            
        usuario_id = st.session_state["usuario_id"]
        
        try:
            # Buscar empréstimos onde o usuário é dono do exemplar
            emprestimos_como_dono = Views.emprestimo_listar_por_dono_exemplar(usuario_id)
            
            if not emprestimos_como_dono:
                st.info("Você não tem empréstimos ativos de seus exemplares.")
                st.write("Quando outros usuários pegarem seus livros emprestados, eles aparecerão aqui.")
                return
            
            st.success(f"Você tem {len(emprestimos_como_dono)} empréstimo(s) ativo(s):")
            
            for emp in emprestimos_como_dono:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        try:
                            # Obter informações detalhadas
                            solicitacao = Views.solicitacao_listar_id(emp[1])
                            exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                            livro = Views.livro_listar_por_id(exemplar[2])
                            solicitante = Views.usuario_listar_por_id(solicitacao[5])
                            
                            if emp[4] is None:  
                                status = "🟢 Ativo"
                                status_color = "green"
                                data_fim = f"Prevista: {emp[3]}"
                            else:
                                status = "Finalizado"
                                status_color = "blue"
                                data_fim = f"Devolvido: {emp[4]}"
                            
                            st.markdown(f"### {livro[1]}")
                            st.markdown(f"**Exemplar:** {exemplar[0]}")
                            st.markdown(f"**Solicitante:** {solicitante[1]}")
                            st.markdown(f"**Início:** {emp[2]}")
                            st.markdown(f"**{data_fim}**")
                            st.markdown(f"**Status:** <span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"Erro ao carregar detalhes: {e}")
                            st.write(f"Empréstimo ID: {emp[0]}")
                    
                    with col2:
                        if emp[4] is None:  # Apenas empréstimos ativos podem solicitar devolução
                            st.write("**Ações:**")
                            if st.button("Ver Detalhes", key=f"detalhes_{emp[0]}", use_container_width=True):
                                st.info(f"Empréstimo {emp[0]} - Livro: {livro[1] if 'livro' in locals() else 'Carregando...'}")
                        else:
                            st.write("**Finalizado**")
                            st.caption("Empréstimo concluído")
            
        except Exception as e:
            st.error(f"Erro ao carregar empréstimos: {str(e)}")

    def Solicitar():
        id_exemplar = st.number_input("Insira o código do exemplar", min_value=1)
        dias_emprestimo = st.number_input("Informe os dias de empréstimo", min_value=1, max_value=30)
        if st.button("Solicitar Empréstimo"):
            try:
                Views.solicitacao_inserir(st.session_state["usuario_id"], id_exemplar, dias_emprestimo)
                st.success("Solicitação de empréstimo realizada com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {str(e)}")

    def SolicitarDevolucao():
        st.subheader("Solicitar Devolução")
        user_emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
        
        emprestimos_ativos = [emp for emp in user_emprestimos if emp[4] is None]
        
        if emprestimos_ativos:
            st.write("Seus empréstimos ativos:")
            for emp in emprestimos_ativos:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Empréstimo ID: {emp[0]}, Data Início: {emp[2]}, Data Prevista: {emp[3]}")
                with col2:
                    if st.button(f"Solicitar Devolução {emp[0]}", key=f"devolver_{emp[0]}"):
                        try:
                            Views.solicitar_devolucao(emp[0])
                            st.success("Devolução solicitada com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
        else:
            st.write("Você não possui empréstimos ativos para devolver")

    def ConfirmarDevolucao(): 
        st.subheader("Confirmar Devolução")
        devolucoes_pendentes = Views.listar_devolucoes_pendentes_por_dono(st.session_state["usuario_id"])
        
        if devolucoes_pendentes:
            st.write("Devoluções pendentes de confirmação:")
            for emp in devolucoes_pendentes:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Empréstimo ID: {emp[0]}, Data Devolução: {emp[4]}")
                with col2:
                    if st.button(f"Confirmar {emp[0]}", key=f"confirmar_{emp[0]}"):
                        try:
                            Views.confirmar_devolucao(emp[0])
                            st.success("Devolução confirmada com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
        else:
            st.write("Não há devoluções pendentes de confirmação")
