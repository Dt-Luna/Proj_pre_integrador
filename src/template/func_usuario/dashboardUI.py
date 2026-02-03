import streamlit as st
from views import Views
import pandas as pd
from datetime import datetime, timedelta

class DashboardUI:
    def main():
        st.title("Dashboard BookShare")
        st.markdown("Bem-vindo ao seu painel principal do BookShare")
        
        # Verificar se usuário está logado
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado para acessar o dashboard.")
            return
        
        # Obter informações do usuário
        try:
            usuario_info = Views.usuario_listar_por_id(st.session_state["usuario_id"])
            nome_usuario = usuario_info[1] if usuario_info else "Usuário"
        except:
            nome_usuario = "Usuário"
        
        st.markdown(f"### Olá, **{nome_usuario}**!")
        
        # Estatísticas principais
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            # Meus exemplares
            meus_exemplares = Views.exemplar_listar_por_usuario(st.session_state["usuario_id"])
            total_meus_exemplares = len(meus_exemplares) if meus_exemplares else 0
            meus_disponiveis = len([ex for ex in meus_exemplares if ex[3] == 'disponivel']) if meus_exemplares else 0
            
            # Minhas solicitações
            minhas_solicitacoes = Views.solicitacao_listar_por_usuario(st.session_state["usuario_id"])
            total_solicitacoes = len(minhas_solicitacoes) if minhas_solicitacoes else 0
            solicitacoes_pendentes = len([s for s in minhas_solicitacoes if s[2] == 'pendente']) if minhas_solicitacoes else 0
            
            # Meus empréstimos ativos
            meus_emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
            emprestimos_ativos = len([e for e in meus_emprestimos if e[4] is None]) if meus_emprestimos else 0
            
            # Solicitações pendentes para mim
            solicitacoes_para_mim = Views.solicitacao_listar_pendentes_por_dono(st.session_state["usuario_id"])
            total_pendentes_aprovar = len(solicitacoes_para_mim) if solicitacoes_para_mim else 0
            
            with col1:
                st.metric("Meus Exemplares", total_meus_exemplares, f"{meus_disponiveis} disponíveis")
            with col2:
                st.metric("Minhas Solicitações", total_solicitacoes, f"{solicitacoes_pendentes} pendentes")
            with col3:
                st.metric("Empréstimos Ativos", emprestimos_ativos)
            with col4:
                st.metric("Aprovações Pendentes", total_pendentes_aprovar)
                
        except Exception as e:
            st.error(f"Erro ao carregar estatísticas: {e}")
        
        st.divider()
        
        # Seções principais
        st.subheader("Atividades Recentes")
        
        # Exibir atividades recentes
        try:
            atividades = []
            
            # Solicitações recentes
            if minhas_solicitacoes:
                solicitacoes_recentes = sorted(minhas_solicitacoes, key=lambda x: x[1], reverse=True)[:3]
                for sol in solicitacoes_recentes:
                    atividades.append(f"Solicitação {sol[2]} - {sol[1]}")
            
            # Empréstimos recentes
            if meus_emprestimos:
                emprestimos_recentes = sorted(meus_emprestimos, key=lambda x: x[2], reverse=True)[:3]
                for emp in emprestimos_recentes:
                    status = "Ativo" if emp[4] is None else "Devolvido"
                    atividades.append(f"Empréstimo {status} - {emp[2]}")
            
            if atividades:
                for atividade in atividades:
                    st.write(f"• {atividade}")
            else:
                st.info("Nenhuma atividade recente")
                
        except Exception as e:
            st.error(f"Erro ao carregar atividades: {e}")
        
        st.divider()
    
        # Avisos e alertas importantes
        try:
            alertas = []
            
            # Verificar empréstimos próximos do vencimento
            if meus_emprestimos:
                for emp in meus_emprestimos:
                    if emp[4] is None and emp[3]:  # Empréstimo ativo com data prevista
                        data_prevista = datetime.strptime(emp[3], "%Y-%m-%d").date()
                        hoje = datetime.now().date()
                        dias_restantes = (data_prevista - hoje).days
                        
                        if dias_restantes <= 3:
                            if dias_restantes < 0:
                                alertas.append(f"Empréstimo {emp[0]} está {abs(dias_restantes)} dias atrasado!")
                            elif dias_restantes == 0:
                                alertas.append(f"Empréstimo {emp[0]} vence hoje!")
                            else:
                                alertas.append(f"Empréstimo {emp[0]} vence em {dias_restantes} dias")
            
            # Verificar solicitações pendentes de aprovação
            if total_pendentes_aprovar > 0:
                alertas.append(f"Você tem {total_pendentes_aprovar} solicitação(ões) pendente(s) de aprovação")
            
            if alertas:
                st.divider()
                st.subheader("Alertas Importantes")
                for alerta in alertas:
                    if "⚠️" in alerta:
                        st.error(alerta)
                    elif "⏰" in alerta:
                        st.warning(alerta)
                    else:
                        st.info(alerta)
                        
        except Exception as e:
            st.error(f"Erro ao verificar alertas: {e}")
