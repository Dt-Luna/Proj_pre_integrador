import streamlit as st
from views import Views
from datetime import datetime, date, timedelta
import pandas as pd
import time

class SolicitacaoUI:
    def main():
        st.title("Solicitações")
        tab1, tab2, tab3 = st.tabs({"Minhas Solicitações", "Solicitar Empréstimo", "Avaliar Solicitações"}) 
        with tab1: SolicitacaoUI.Ver()
        with tab2: SolicitacaoUI.Solicitar()
        with tab3: SolicitacaoUI.Avaliar()


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
        solicitacoes = Views.solicitacao_listar_por_exemplar() #essa função não existe na Views, poderia criar prfvr?☢️
        #acredito que o mais direto/ ideal seria "solicitacao_listar_por_dono", mas o dono não tem o id no objeto Solicitacao, mas o id_emprestimo é capas de fazer esse link, então, fora o link em empréstimo, um outro link para retornar uma lista dos empréstimo de usuário X ☢️☢️☢️
        if solicitacoes:
            
        else: st.write("Não há solicitação pendente de seus exemplares")

    def Solicitar(): #criar uma solicitação de emprestimo de exemplar dozoto
        id_exemplar = st.number_input("Insira o código do exemplar")
        data_inicio = st.date_input("Informe a data de início do empréstimo", min_value=date.today(), max_value=date(date.today().year+1, 6, 1))
        data_prevista = st.date_input("Informe a data prevista de devolução", min_value=date.today(), max_value=date(date.today().year+1, 6, 1))
        if st.button("Solicitar Empréstimo"):

            dias_emprestimo = data_inicio - data_prevista
            Views.emprestimo_inserir( st.session_state["usuario_id"], id_exemplar, dias_emprestimo)
            st.success("Solicitação de empréstico realizada com sucesso!")
            time.sleep(2)
            st.rerun()
