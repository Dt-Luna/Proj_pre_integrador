import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd
import time

class AvaliarUI:
    def main():
        st.title("Avaliar")
        tab1, tab2 = st.tabs(["Criar Avaliação", "Avaliados"])
        with tab1: AvaliarUI.Criar()
        with tab2: AvaliarUI.avaliados()

    def Criar():
        #Avaliar se o usuário tem movimento, se emprestou algo ou se pegou emprestado☢️

        tipo_avaliador = st.radio(
            "Quem é você?",
            ('Dono do Exemplar', 'Comodatário do exemplar')
        )
        nota = st.feedback("stars") #cria uma linha de 5 estrelas. retorna indice de 0 a 4
        comentario = st.text_area()

        if st.button("Enviar Avaliação"):
            #adicionar except☢️

            match tipo_avaliador:
                case "Comodatário do exemplar": tipo_avaliador = 1
                case "'Dono do Exemplar": tipo_avaliador = 2
                case _: tipo_avaliador = 2

            Views.avaliacao_inserir(None, st.session_state["usuario_id"], tipo_avaliador, nota + 1, comentario, datetime.now())
            st.success("Usuário avaliado com sucesso!")
            time.sleep(2)
            st.rerun()

    def avaliados():
        emprestimos = Views.emprestimo_listar()
        if len(emprestimos) == 0: st.write("Não há empréstimos cadastrados")
        else:
            id_emprestimo = st.number_input("Insira o código do emprestimo: ")
            if st.button("Submeter"):
                user_avaliados = Views.avaliacao_listar_id(st.session_state["usuario_id"], id_emprestimo)

                list_dic = []
                for obj in user_avaliados: list_dic.append(obj.to_df())
                df = pd.DataFrame(list_dic)
                st.dataframe(df)
