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
        # Listar empréstimos finalizados para avaliação
        emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
        emprestimos_finalizados = [e for e in emprestimos if e[4] is not None]  # data_devolucao not None

        if not emprestimos_finalizados:
            st.write("Nenhum empréstimo finalizado para avaliar.")
            return

        opcoes = [f"Empréstimo ID: {e[0]}, Solicitação: {e[1]}" for e in emprestimos_finalizados]
        emprestimo_selecionado = st.selectbox("Selecione o empréstimo para avaliar", opcoes)
        id_emprestimo = emprestimos_finalizados[opcoes.index(emprestimo_selecionado)][0]

        # Verificar se já avaliou
        existing = Views.avaliacao_listar_por_avaliador_emprestimo(st.session_state["usuario_id"], id_emprestimo)
        if existing:
            st.write("Você já avaliou este empréstimo.")
            return

        tipo_avaliador = st.radio(
            "Quem é você?",
            ('Dono do Exemplar', 'Comodatário do exemplar')
        )
        nota = st.feedback("stars")  # retorna índice de 0 a 4
        comentario = st.text_area("Comentário (opcional): ", "")

        if st.button("Enviar Avaliação"):
            try:
                tipo = 1 if tipo_avaliador == 'Comodatário do exemplar' else 2
                Views.avaliacao_inserir(st.session_state["usuario_id"], tipo, nota + 1, comentario, id_emprestimo)
                st.success("Avaliação enviada com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {str(e)}")

    def avaliados():
        emprestimos = Views.emprestimo_listar()
        if len(emprestimos) == 0: st.write("Nenhum empréstimos a avaliar")
        else:
            id_emprestimo = st.number_input("Insira o código do emprestimo: ")
            if st.button("Submeter"):
                user_avaliados = Views.avaliacao_listar_id(st.session_state["usuario_id"], id_emprestimo)

                list_dic = []
                for obj in user_avaliados: list_dic.append(obj.to_df())
                df = pd.DataFrame(list_dic)
                st.dataframe(df)
