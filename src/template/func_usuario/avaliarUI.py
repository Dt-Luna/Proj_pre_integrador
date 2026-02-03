import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd
import time

class AvaliarUI:
    def main():
        st.title("Avaliações")
        tab1, tab2, tab3 = st.tabs(["Criar Avaliação", "Minhas Avaliações", "Avaliações Recebidas"])
        with tab1: AvaliarUI.Criar()
        with tab2: AvaliarUI.avaliados()
        with tab3: AvaliarUI.avaliacoes_recebidas()

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
        try:
            # Listar todas as avaliações do usuário atual
            avaliacoes = Views.avaliacao_listar()
            minhas_avaliacoes = [a for a in avaliacoes if a[1] == st.session_state["usuario_id"]]
            
            if not minhas_avaliacoes:
                st.write("Você ainda não fez nenhuma avaliação.")
                return
            
            # Exibir avaliações em formato de DataFrame
            dados_avaliacoes = []
            for avaliacao in minhas_avaliacoes:
                id_avaliacao = avaliacao[0]
                id_emprestimo = avaliacao[5]
                nota = avaliacao[3]
                comentario = avaliacao[4]
                tipo = "Dono" if avaliacao[2] == 2 else "Comodatário"
                
                # Obter informações do empréstimo
                emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                
                dados_avaliacoes.append({
                    "ID Avaliação": id_avaliacao,
                    "Livro": livro[1],
                    "Nota": "⭐" * nota,
                    "Tipo": tipo,
                    "Comentário": comentario or "Sem comentário"
                })
            
            df = pd.DataFrame(dados_avaliacoes)
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações: {str(e)}")

    def avaliacoes_recebidas():
        st.subheader("Avaliações Recebidas")
        st.write("Avaliações que outros usuários fizeram sobre seus exemplares emprestados.")
        
        try:
            # Listar avaliações recebidas pelo usuário
            avaliacoes_recebidas = Views.avaliacao_listar_por_dono_exemplar(st.session_state["usuario_id"])
            
            if not avaliacoes_recebidas:
                st.info("Você ainda não recebeu nenhuma avaliação.")
                return
            
            # Exibir avaliações recebidas
            dados_avaliacoes = []
            for avaliacao in avaliacoes_recebidas:
                id_avaliador = avaliacao[0]
                tipo_avaliador = avaliacao[1]
                nota = avaliacao[2]
                comentario = avaliacao[3]
                id_emprestimo = avaliacao[4]
                data_avaliacao = avaliacao[5]
                
                # Obter informações do avaliador
                avaliador_info = Views.usuario_listar_por_id(id_avaliador)
                nome_avaliador = avaliador_info[1] if avaliador_info else "Usuário desconhecido"
                
                # Obter informações do empréstimo e livro
                emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                
                # Determinar tipo de avaliador
                if tipo_avaliador == 1:
                    tipo = "Comodatário"
                else:
                    tipo = "Dono"
                
                dados_avaliacoes.append({
                    "ID Avaliador": id_avaliador,
                    "Livro": livro[1],
                    "Avaliador": nome_avaliador,
                    "Nota": "⭐" * nota,
                    "Tipo": tipo,
                    "Comentário": comentario or "Sem comentário",
                    "Data": data_avaliacao
                })
            
            # Exibir estatísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_avaliacoes = len(dados_avaliacoes)
                st.metric("Total Avaliações", total_avaliacoes)
            
            with col2:
                if dados_avaliacoes:
                    media_notas = sum([len(d["Nota"]) for d in dados_avaliacoes]) / total_avaliacoes
                    st.metric("⭐ Média Notas", f"{media_notas:.1f}")
                else:
                    st.metric("⭐ Média Notas", "0.0")
            
            with col3:
                if dados_avaliacoes:
                    avaliacoes_5_estrelas = len([d for d in dados_avaliacoes if len(d["Nota"]) == 5])
                    st.metric("🌟 5 Estrelas", avaliacoes_5_estrelas)
                else:
                    st.metric("🌟 5 Estrelas", 0)
            
            # Exibir tabela de avaliações
            st.subheader("Detalhes das Avaliações")
            df = pd.DataFrame(dados_avaliacoes)
            st.dataframe(df, use_container_width=True)
            
            # Exibir avaliações recentes em cards
            st.subheader("Avaliações Recentes")
            for avaliacao in dados_avaliacoes[:3]:  # Mostrar apenas as 3 mais recentes
                with st.container(border=True):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"### {avaliacao['Nota']}")
                        st.caption(avaliacao['Tipo'])
                    with col2:
                        st.markdown(f"**{avaliacao['Livro']}**")
                        st.markdown(f"*por {avaliacao['Avaliador']}*")
                        if avaliacao['Comentário'] != "Sem comentário":
                            st.write(f"{avaliacao['Comentário']}")
                        st.caption(f"{avaliacao['Data']}")
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações recebidas: {str(e)}")
