import streamlit as st
from views import Views
from datetime import datetime
import pandas as pd
import time

class AvaliarUI:
    @staticmethod
    def main():
        st.title("Avaliações")
        tab1, tab2, tab3 = st.tabs(["Criar Avaliação", "Minhas Avaliações", "Avaliações Recebidas"])
        with tab1: AvaliarUI.Criar()
        with tab2: AvaliarUI.avaliados()
        with tab3: AvaliarUI.avaliacoes_recebidas()

    @staticmethod
    def Criar():
        st.subheader("Criar Avaliação")
        st.write("Avalie empréstimos que você participou como solicitante ou como dono do exemplar.")
        
        emprestimos = Views.emprestimo_listar_por_usuario(st.session_state["usuario_id"])
        emprestimos_finalizados = [e for e in emprestimos if e[4] is not None]  # data_devolucao not None

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

    @staticmethod
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
                
                if eh_anonimo:
                    nome_avaliado = "Anônimo"
                else:
                    try:
                        if solicitacao[5] == st.session_state["usuario_id"]:
                            avaliado_info = Views.usuario_listar_por_id(exemplar[1])
                            nome_avaliado = avaliado_info[1] if avaliado_info else "Usuário desconhecido"
                        else:
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

    @staticmethod
    def avaliacoes_recebidas():
        st.subheader("Avaliações Recebidas")
        st.write("Avaliações que outros usuários fizeram sobre você em empréstimos realizados.")
        
        try:
            avaliacoes = Views.avaliacao_listar()
            # Estrutura: [id_avaliador, tipo_avaliador, nota, comentario, id_emprestimo, data_avaliacao, anonimo]
            avaliacoes_recebidas = []
            avaliacoes_como_dono = []
            avaliacoes_como_comodatario = []
            
            for avaliacao in avaliacoes:
                if avaliacao[0] != st.session_state["usuario_id"]:
                    try:
                        id_emprestimo = avaliacao[4]
                        emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                        solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                        id_exemplar = solicitacao[4]
                        id_solicitante = solicitacao[5]
                        
                        meus_exemplares = Views.exemplar_listar_por_usuario(st.session_state["usuario_id"])
                        if any(ex[0] == id_exemplar for ex in meus_exemplares):
                            avaliacoes_como_dono.append(avaliacao)
                        
                        elif id_solicitante == st.session_state["usuario_id"]:
                            avaliacoes_como_comodatario.append(avaliacao)
                        
                    except:
                        continue
            
            st.markdown("---")
            st.subheader("Avaliações como Dono do Exemplar")
            st.write("Comodatários avaliando seus exemplares:")
            
            if not avaliacoes_como_dono:
                st.info("Você ainda não recebeu nenhuma avaliação como dono de exemplar.")
            else:
                dados_avaliacoes_dono = []
                for avaliacao in avaliacoes_como_dono:
                    dados = AvaliarUI._processar_avaliacao(avaliacao)
                    if dados:
                        dados_avaliacoes_dono.append(dados)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(dados_avaliacoes_dono))
                with col2:
                    if dados_avaliacoes_dono:
                        media = sum(d["Nota Numérica"] for d in dados_avaliacoes_dono) / len(dados_avaliacoes_dono)
                        st.metric("⭐ Média", f"{media:.1f}")
                    else:
                        st.metric("⭐ Média", "0.0")
                with col3:
                    if dados_avaliacoes_dono:
                        cinco_estrelas = len([d for d in dados_avaliacoes_dono if d["Nota Numérica"] == 5])
                        st.metric("🌟 5 Estrelas", cinco_estrelas)
                    else:
                        st.metric("🌟 5 Estrelas", 0)
                
                df_dono = pd.DataFrame(dados_avaliacoes_dono)
                st.dataframe(df_dono, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Avaliações como Comodatário")
            st.write("Donos de exemplares avaliando você como comodatário:")
            
            if not avaliacoes_como_comodatario:
                st.info("Você ainda não recebeu nenhuma avaliação como comodatário.")
            else:
                dados_avaliacoes_comodatario = []
                for avaliacao in avaliacoes_como_comodatario:
                    dados = AvaliarUI._processar_avaliacao(avaliacao)
                    if dados:
                        dados_avaliacoes_comodatario.append(dados)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(dados_avaliacoes_comodatario))
                with col2:
                    if dados_avaliacoes_comodatario:
                        media = sum(d["Nota Numérica"] for d in dados_avaliacoes_comodatario) / len(dados_avaliacoes_comodatario)
                        st.metric("⭐ Média", f"{media:.1f}")
                    else:
                        st.metric("⭐ Média", "0.0")
                with col3:
                    if dados_avaliacoes_comodatario:
                        cinco_estrelas = len([d for d in dados_avaliacoes_comodatario if d["Nota Numérica"] == 5])
                        st.metric("🌟 5 Estrelas", cinco_estrelas)
                    else:
                        st.metric("🌟 5 Estrelas", 0)
                
                df_comodatario = pd.DataFrame(dados_avaliacoes_comodatario)
                st.dataframe(df_comodatario, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações: {str(e)}")

    @staticmethod
    def _processar_avaliacao(avaliacao):
        """Método auxiliar para processar dados de uma avaliação"""
        try:
            id_avaliador = avaliacao[0]
            tipo_avaliador = avaliacao[1]
            nota = avaliacao[2]
            comentario = avaliacao[3]
            id_emprestimo = avaliacao[4]
            data_avaliacao = avaliacao[5]
            eh_anonimo = bool(avaliacao[6]) if len(avaliacao) > 6 else False
            
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
            
            return {
                "ID Avaliador": id_avaliador,
                "Livro": livro[1],
                "Avaliador": nome_avaliador,
                "Nota": "⭐" * nota,
                "Nota Numérica": nota,
                "Tipo": tipo,
                "Comentário": comentario or "Sem comentário",
                "Data": data_avaliacao or "Não informada",
                "Anônimo": "Sim" if eh_anonimo else "Não"
            }
        except:
            return None
