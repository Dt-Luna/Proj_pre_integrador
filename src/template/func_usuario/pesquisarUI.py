import streamlit as st
import pandas as pd
from datetime import datetime
from views import Views
import time

class PesquisarUI:
    @staticmethod
    def main():
        st.header("🔍 Pesquisar Livros e Solicitar Empréstimo")
        
        # 1. Obter dados e fazer a pesquisa
        livros = Views.livro_listar()
        
        # Opcional: Criar DataFrame com nomes de colunas amigáveis
        # Assumindo que livros é uma lista de tuplas: (id, titulo, autor, genero)
        if not livros:
             st.info("Nenhum livro cadastrado.")
             return

        df_livros = pd.DataFrame(livros, columns=['ID', 'Título', 'Autor', 'Páginas', 'ISBN'])
        
        termo = st.text_input("Digite o termo de pesquisa (título, autor, gênero):")
        
        # Filtragem
        if termo:
            mask = (
                df_livros['Título'].str.contains(termo, case=False) |
                df_livros['Autor'].str.contains(termo, case=False)
            )
            df_filtrado = df_livros[mask]
        else:
            df_filtrado = df_livros

        # 2. Exibir DataFrame Interativo (Seleção de Linha)
        st.write("Selecione um livro na tabela abaixo para ver os exemplares disponíveis:")
        
        # Evento de seleção (Disponível no Streamlit 1.35+)
        event = st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",  # Recarrega a página ao selecionar
            selection_mode="single-row"
        )

        # 3. Lógica ao Selecionar um Livro
        if event.selection.rows:
            # Pegar o índice da linha selecionada
            idx_selecionado = event.selection.rows[0]
            # Pegar os dados do livro usando o índice no dataframe filtrado
            livro_selecionado = df_filtrado.iloc[idx_selecionado]
            id_livro = livro_selecionado['ID']
            st.write(id_livro)
            titulo_livro = livro_selecionado['Título']

            st.divider()
            st.subheader(f"📖 Exemplares de: {titulo_livro}")

            # Buscar exemplares deste livro (Necessário implementar no Views)
            # Retorno esperado: lista de (id_exemplar, id_livro, disponivel_bool, codigo_fisico)
            exemplares = Views.exemplar_listar_por_livro(id_livro)
            
            if not exemplares:
                st.warning("Nenhum exemplar cadastrado para este livro.")
            else:
                # Exibir exemplares em formato de cartões ou lista
                for exemplar in exemplares:
                    id_exemplar = exemplar[0]
                    disponivel = exemplar[2] # Assumindo booleano ou string 'Disponível'
                    
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Cód. Exemplar:** {id_exemplar}")
                            status_icon = "🟢" if disponivel else "🔴"
                            status_text = "Disponível" if disponivel else "Indisponível/Emprestado"
                            st.write(f"Status: {status_icon} {status_text}")

                        with col2:
                            if disponivel:
                                # Botão com chave única para evitar conflitos
                                if st.button("Alugar", key=f"btn_{id_exemplar}"):
                                    PesquisarUI.realizar_emprestimo(id_exemplar)
                            else:
                                st.button("Indisponível", disabled=True, key=f"btn_d_{id_exemplar}")

    @staticmethod
    def realizar_emprestimo(id_exemplar):
        """Método auxiliar para processar o empréstimo"""
        # Verifica se existe usuário logado
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado para alugar um livro.")
            return

        id_usuario = st.session_state["usuario_id"]
        
        # Chama a view para inserir no banco
        # Assumindo que retorna True se der certo, ou uma mensagem de erro
        sucesso = Views.emprestimo_inserir(id_exemplar, id_usuario, )
        
        if sucesso:
            st.success("Empréstimo realizado com sucesso!")
            time.sleep(2)
            st.rerun() # Atualiza a tela para mostrar o livro como indisponível
        else:
            st.error("Erro ao realizar empréstimo. Tente novamente.")