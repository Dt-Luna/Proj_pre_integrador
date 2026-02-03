import streamlit as st
from views import Views
from datetime import datetime, date, timedelta
import pandas as pd
import time

class SolicitacaoUI:
    def main():
        st.title("Solicitações")
        tab1, tab2, tab3, tab4, tab5 = st.tabs({"Minhas Solicitações", "Solicitar Empréstimo", "Avaliar Solicitações", "Solicitar Devolução", "Confirmar Devolução"})
        with tab1: SolicitacaoUI.Ver()
        with tab2: SolicitacaoUI.Solicitar()
        with tab3: SolicitacaoUI.Avaliar()
        with tab4: SolicitacaoUI.SolicitarDevolucao()
        with tab5: SolicitacaoUI.ConfirmarDevolucao()


    def Ver(): #solicitações suas para outros livros. terá principalmente o status na tabela.
        user_solicitacoes = Views.solicitacao_listar_por_usuario(st.session_state["usuario_id"]) #essa função não existe na Views, poderia criar prfvr?☢️
        if user_solicitacoes:
            list_dic = []
            for obj in user_solicitacoes: list_dic.append(obj.to_df())
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

        else:
            st.write("Ainda não foi submetida solicitação de empréstimo")

    def Avaliar(): #avaliar a solicitação dos outros para/ com os seus exemplares para criar um empréstimo.
        solicitacoes = Views.solicitacao_listar_pendentes_por_dono(st.session_state["usuario_id"])
        if solicitacoes:
            for obj in solicitacoes:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"Solicitação ID: {obj[0]}, Data: {obj[1]}, Status: {obj[2]}, Dias: {obj[3]}, Exemplar: {obj[4]}, Solicitante: {obj[5]}")
                with col2:
                    if st.button(f"Aprovar {obj[0]}", key=f"aprovar_{obj[0]}"):
                        try:
                            Views.aprovar_solicitacao(obj[0])
                            st.success("Solicitação aprovada!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
                with col3:
                    if st.button(f"Rejeitar {obj[0]}", key=f"rejeitar_{obj[0]}"):
                        try:
                            Views.rejeitar_solicitacao(obj[0])
                            st.success("Solicitação rejeitada!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
        else:
            st.write("Não há solicitação pendente de seus exemplares")

    def Solicitar(): #criar uma solicitação de emprestimo de exemplar do outro
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
