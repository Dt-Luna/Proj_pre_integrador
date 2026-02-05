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
        st.subheader("Criar Avaliação")
        st.write("Avalie empréstimos que você participou como solicitante ou como dono do exemplar.")
        
        # Listar empréstimos finalizados para avaliação
        emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
        emprestimos_finalizados = [e for e in emprestimos if e[4] is not None]  # data_devolucao not None

        # Também buscar empréstimos onde o usuário é dono do exemplar
        todos_emprestimos = Views.emprestimo_listar()
        emprestimos_como_dono = []
        
        for emp in todos_emprestimos:
            if emp[4] is not None:
                solicitacao = Views.solicitacao_listar_id(emp[1])
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                if exemplar and exemplar[1] == st.session_state["usuario_id"]:
                    emprestimos_como_dono.append(emp)

        todos_emprestimos_avaliaveis = emprestimos_finalizados + emprestimos_como_dono

        if not todos_emprestimos_avaliaveis:
            st.info("Nenhum empréstimo finalizado para avaliar.")
            st.write("Você só pode avaliar empréstimos que já foram concluídos.")
            return

        opcoes = []
        detalhes_emprestimos = []
        
        for e in todos_emprestimos_avaliaveis:
            try:
                solicitacao = Views.solicitacao_listar_id(e[1])
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                solicitante = Views.usuario_listar_por_id(solicitacao[5])
                
                # Verificar se já avaliou
                existing = Views.avaliacao_listar_por_avaliador_emprestimo(st.session_state["usuario_id"], e[0])
                avaliado_texto = "Já avaliado" if existing else ""
                
                detalhe = {
                    'emprestimo': e,
                    'livro': livro[1],
                    'exemplar_id': exemplar[0],
                    'solicitante': solicitante[1],
                    'data_devolucao': e[4],
                    'avaliado': existing is not None
                }
                
                if e in emprestimos_finalizados:
                    opcoes.append(f"Como Comodatário - {livro[1]} (ID: {e[0]}){avaliado_texto}")
                    detalhe['tipo'] = 'Comodatário'
                else:
                    opcoes.append(f"Como Dono - {livro[1]} (ID: {e[0]}){avaliado_texto}")
                    detalhe['tipo'] = 'Dono'
                
                detalhes_emprestimos.append(detalhe)
                
            except Exception as err:
                st.error(f"Erro ao processar empréstimo {e[0]}: {err}")
                continue

        opcoes_disponiveis = []
        indices_disponiveis = []
        
        for i, detalhe in enumerate(detalhes_emprestimos):
            if not detalhe['avaliado']:
                opcoes_disponiveis.append(opcoes[i])
                indices_disponiveis.append(i)

        if not opcoes_disponiveis:
            st.success("Todos os seus empréstimos já foram avaliados! 🎉")
            return
        
        st.write(f"**Empréstimos disponíveis para avaliação:** {len(opcoes_disponiveis)}")
        
        emprestimo_selecionado = st.selectbox("Selecione o empréstimo para avaliar", opcoes_disponiveis)
        indice_original = indices_disponiveis[opcoes_disponiveis.index(emprestimo_selecionado)]
        
        detalhe_selecionado = detalhes_emprestimos[indice_original]
        id_emprestimo = detalhe_selecionado['emprestimo'][0]
        
        st.markdown("---")
        st.markdown("### Detalhes do Empréstimo")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Livro:** {detalhe_selecionado['livro']}")
            st.markdown(f"**Exemplar:** {detalhe_selecionado['exemplar_id']}")
            st.markdown(f"**Solicitante:** {detalhe_selecionado['solicitante']}")
        
        with col2:
            st.markdown(f"**Sua relação:** {detalhe_selecionado['tipo']}")
            st.markdown(f"**Data devolução:** {detalhe_selecionado['data_devolucao']}")
        
        if detalhe_selecionado['tipo'] == 'Comodatário':
            tipo_avaliador_default = 'Comodatário do exemplar'
            st.info("Você está avaliando como **comodatário** - quem pegou o livro emprestado")
        else:
            tipo_avaliador_default = 'Dono do Exemplar'
            st.info("Você está avaliando como **dono** - quem emprestou o livro")

        st.markdown("---")
        st.markdown("### Criar Avaliação")

        col1, col2 = st.columns(2)
        
        with col1:
            tipo_avaliador = st.radio(
                "Qual seu papel neste empréstimo?",
                ('Dono do Exemplar', 'Comodatário do exemplar'),
                help="Dono = você emprestou o livro | Comodatário = você pegou o livro emprestado"
            )
        
        with col2:
            anonimo = st.checkbox(
                "Avaliação anônima",
                help="Sua identidade não será revelada ao avaliado"
            )

        nota = st.feedback("stars")
        comentario = st.text_area("Comentário (opcional): ", "")

        if st.button("Enviar Avaliação"):
            try:
                tipo = 1 if tipo_avaliador == 'Comodatário do exemplar' else 2
                Views.avaliacao_inserir(
                    st.session_state["usuario_id"], 
                    tipo, 
                    nota + 1, 
                    comentario, 
                    id_emprestimo,
                    anonimo
                )
                st.success("Avaliação enviada com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {str(e)}")

    def avaliados():
        try:
            avaliacoes = Views.avaliacao_listar()
            # Estrutura: [id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao, anonimo]
            minhas_avaliacoes = [a for a in avaliacoes if a[0] == st.session_state["usuario_id"]]
            
            if not minhas_avaliacoes:
                st.write("Você ainda não fez nenhuma avaliação.")
                return
            
            dados_avaliacoes = []
            for avaliacao in minhas_avaliacoes:
                # Estrutura correta: [id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao, anonimo]
                id_avaliador = avaliacao[0]
                tipo_avaliador = avaliacao[1]
                nota = avaliacao[2]
                comentario = avaliacao[3]
                id_emprestimo = avaliacao[4]
                data_avaliacao = avaliacao[5]
                eh_anonimo = bool(avaliacao[6]) if len(avaliacao) > 6 else False
                
                tipo = "Dono" if tipo_avaliador == 2 else "Comodatário"
                
                emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                
                # Obter informações do avaliado
                if eh_anonimo:
                    nome_avaliado = "Anônimo"
                else:
                    try:
                        # O avaliado é o outro participante do empréstimo
                        if solicitacao[5] == st.session_state["usuario_id"]:
                            # Usuário atual foi o solicitante, então o avaliado é o dono
                            avaliado_info = Views.usuario_listar_por_id(exemplar[1])
                            nome_avaliado = avaliado_info[1] if avaliado_info else "Usuário desconhecido"
                        else:
                            # Usuário atual foi o dono, então o avaliado é o solicitante
                            avaliado_info = Views.usuario_listar_por_id(solicitacao[5])
                            nome_avaliado = avaliado_info[1] if avaliado_info else "Usuário desconhecido"
                    except:
                        nome_avaliado = "Usuário desconhecido"
                
                dados_avaliacoes.append({
                    "ID Avaliador": id_avaliador,
                    "Livro": livro[1],
                    "Avaliado": nome_avaliado,
                    "Nota": "⭐" * nota,
                    "Nota Numérica": nota,
                    "Tipo": tipo,
                    "Comentário": comentario or "Sem comentário",
                    "Data": data_avaliacao or "Não informada",
                    "Anônimo": "Sim" if eh_anonimo else "Não"
                })
            
            df = pd.DataFrame(dados_avaliacoes)
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações: {str(e)}")

    def avaliacoes_recebidas():
        st.subheader("Avaliações Recebidas")
        st.write("Avaliações que outros usuários fizeram sobre você em empréstimos realizados.")
        
        try:
            # Buscar empréstimos do usuário atual (onde ele foi solicitante)
            meus_emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
            
            if not meus_emprestimos:
                st.info("Você não realizou nenhum empréstimo ainda.")
                return
            
            # Buscar avaliações sobre esses empréstimos
            todas_avaliacoes = Views.avaliacao_listar()
            avaliacoes_recebidas = []
            
            for avaliacao in todas_avaliacoes:
                id_emprestimo = avaliacao[4]
                id_avaliador = avaliacao[0]  # id_avaliador está no índice 0
                
                # Verificar se esta avaliação é sobre um empréstimo do usuário atual
                if any(emp[0] == id_emprestimo for emp in meus_emprestimos):
                    # Verificar se o avaliador não é o próprio usuário
                    if id_avaliador != st.session_state["usuario_id"]:
                        avaliacoes_recebidas.append(avaliacao)
            
            if not avaliacoes_recebidas:
                st.info("Você ainda não recebeu nenhuma avaliação sobre seus empréstimos.")
                return
            
            dados_avaliacoes = []
            for avaliacao in avaliacoes_recebidas:  # Usar apenas as avaliações recebidas filtradas
                # Estrutura correta: [id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao, anonimo]
                id_avaliador = avaliacao[0]
                tipo_avaliador = avaliacao[1]
                nota = avaliacao[2]
                comentario = avaliacao[3]
                id_emprestimo = avaliacao[4]
                data_avaliacao = avaliacao[5]
                eh_anonimo = bool(avaliacao[6]) if len(avaliacao) > 6 else False
                
                # Obter informações do avaliador (se não for anônimo)
                if eh_anonimo:
                    nome_avaliador = "Anônimo"
                else:
                    try:
                        avaliador_info = Views.usuario_listar_por_id(id_avaliador)
                        nome_avaliador = avaliador_info[1] if avaliador_info else "Usuário desconhecido"
                    except:
                        nome_avaliador = f"Usuário {id_avaliador} (inativo)"
                
                emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                exemplar = Views.exemplar_listar_por_id(solicitacao[4])
                livro = Views.livro_listar_por_id(exemplar[2])
                
                if tipo_avaliador == 1:
                    tipo = "Comodatário"
                else:
                    tipo = "Dono do Exemplar"
                
                dados_avaliacoes.append({
                    "ID Avaliador": id_avaliador,
                    "Livro": livro[1],
                    "Avaliador": nome_avaliador,
                    "Nota": "⭐" * nota,
                    "Nota Numérica": nota,
                    "Tipo": tipo,
                    "Comentário": comentario or "Sem comentário",
                    "Data": data_avaliacao or "Não informada",
                    "Anônimo": "Sim" if eh_anonimo else "Não"
                })
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_avaliacoes = len(dados_avaliacoes)
                st.metric("Total Avaliações", total_avaliacoes)
            
            with col2:
                if dados_avaliacoes:
                    media_notas = sum([d["Nota Numérica"] for d in dados_avaliacoes]) / total_avaliacoes
                    st.metric("⭐ Média Notas", f"{media_notas:.1f}")
                else:
                    st.metric("⭐ Média Notas", "0.0")
            
            with col3:
                if dados_avaliacoes:
                    avaliacoes_5_estrelas = len([d for d in dados_avaliacoes if d["Nota Numérica"] == 5])
                    st.metric("🌟 5 Estrelas", avaliacoes_5_estrelas)
                else:
                    st.metric("🌟 5 Estrelas", 0)
            
            st.subheader("Detalhes das Avaliações")
            df = pd.DataFrame(dados_avaliacoes)
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Avaliações Recentes")
            for avaliacao in dados_avaliacoes[:3]:  # Mostrar apenas as 3 mais recentes
                with st.container(border=True):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"### {avaliacao['Nota']}")
                        st.caption(avaliacao['Tipo'])
                        if avaliacao['Anônimo'] == 'Sim':
                            st.caption("Avaliação anônima")
                    with col2:
                        st.markdown(f"**{avaliacao['Livro']}**")
                        if avaliacao['Anônimo'] == 'Não':
                            st.markdown(f"*por {avaliacao['Avaliador']}*")
                        else:
                            st.markdown("*por usuário anônimo*")
                        if avaliacao['Comentário'] != "Sem comentário":
                            st.write(f"{avaliacao['Comentário']}")
                        st.caption(f"{avaliacao['Data']}")
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações recebidas: {str(e)}")
