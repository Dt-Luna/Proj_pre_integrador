import streamlit as st
from views import Views
from datetime import datetime
from pandas import DataFrame

class CRUD_avalicao:
    def main():
        st.title("Avaliações")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar Avaliações", "Adicionar Avaliação", "Atualizar Avaliação", "Excluir Avaliação"])
        with tab1: CRUD_avalicao.listar_avaliacoes()
        with tab2: CRUD_avalicao.adicionar_avaliacao()
        with tab3: CRUD_avalicao.atualizar_avaliacao()
        with tab4: CRUD_avalicao.excluir_avaliacao()

    def listar_avaliacoes():
        st.header("Listar Avaliações")
        try:
            avaliacoes = Views.avaliacao_listar()
            if avaliacoes:
                df = DataFrame(avaliacoes, columns=["ID Avaliação", "ID Avaliador", "Tipo Avaliador", "Nota", "Comentário", "ID Empréstimo", "Data Avaliação"])
                st.dataframe(df)
            else:
                st.info("Nenhuma avaliação encontrada.")

            # referencia pra tabela
                        # list_dic = []
            # for obj in profissionais: list_dic.append(obj.to_json())
            # df = pd.DataFrame(list_dic)
            # st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao listar avaliações: {e}")

    def adicionar_avaliacao():
        st.header("Adicionar Avaliação")
        emprestimos = Views.emprestimo_listar()
        op = st.selectbox("Selecione o Empréstimo para Avaliar", emprestimos)
        id_emprestimo = op[0] if op else None
        tipo_avaliador = st.text_input("Tipo do Avaliador (usuário/administrador)")
        nota = st.number_input("Nota (1-5)", min_value=1, max_value=5)
        comentario = st.text_area("Comentário")
        data_avaliacao = st.text_input("Data da Avaliação (AAAA-MM-DD)", value=datetime.now().strftime("%Y-%m-%d"))

        if st.button("Adicionar Avaliação"):
            try:
                Views.avaliacao_inserir(id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao)
                st.success("Avaliação adicionada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar avaliação: {e}")

    def atualizar_avaliacao():
        st.header("Atualizar Avaliação")
        id = st.text_input("ID da Avaliação a ser Atualizada")
        id_avaliador = st.text_input("Novo ID do Avaliador")
        tipo_avaliador = st.text_input("Novo Tipo do Avaliador (usuário/administrador)")
        nota = st.number_input("Nova Nota (1-5)", min_value=1, max_value=5)
        comentario = st.text_area("Novo Comentário")
        id_emprestimo = st.text_input("Novo ID do Empréstimo")
        data_avaliacao = st.text_input("Nova Data da Avaliação (AAAA-MM-DD)", value=datetime.now().strftime("%Y-%m-%d"))

        if st.button("Atualizar Avaliação"):
            try:
                Views.avaliacao_atualizar(id, id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao)
                st.success("Avaliação atualizada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao atualizar avaliação: {e}")

    def excluir_avaliacao():
        st.header("Excluir Avaliação")
        id = st.text_input("ID da Avaliação a ser Excluída")

        if st.button("Excluir Avaliação"):
            try:
                Views.avaliacao_excluir(id)
                st.success("Avaliação excluída com sucesso!")
            except Exception as e:
                st.error(f"Erro ao excluir avaliação: {e}")