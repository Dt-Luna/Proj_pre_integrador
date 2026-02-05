import streamlit as st
from views import Views
import pandas as pd
import time

class VisualizarPerfilUI:
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

    @staticmethod
    def main():
        st.title("Visualizar Perfil de Usuário")
        
        busca = st.text_input("Buscar usuário por email ou username:")
        
        if busca:
            try:
                usuario = Views.usuario_listar_por_email(busca)
                if not usuario:
                    usuario = Views.usuario_listar_por_username(busca)
                
                if not usuario:
                    st.error("Usuário não encontrado.")
                    return
                
                VisualizarPerfilUI.exibir_perfil(usuario)
                
            except Exception as e:
                st.error(f"Erro ao buscar usuário: {str(e)}")
    
    @staticmethod
    def exibir_perfil(usuario):
        """Exibe informações do perfil de um usuário"""
        st.write(f"DEBUG: Iniciando exibir_perfil para usuário: {usuario}")
        
        id_usuario = usuario[0]
        username = usuario[1]
        data_nascimento = usuario[3]
        email = usuario[4]
        
        st.subheader(f"👤 {username}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Informações Pessoais:**")
            st.write(f"**Email:** {email}")
            st.write(f"**Data de Nascimento:** {data_nascimento}")
        
        with col2:
            st.markdown("**Estatísticas:**")
            exemplares = Views.exemplar_listar_por_usuario(id_usuario)
            st.write(f"**Exemplares na Biblioteca:** {len(exemplares)}")
            
            avaliacoes = Views.avaliacao_listar()
            avaliacoes_usuario = [a for a in avaliacoes if a[1] == id_usuario]
            st.write(f"**Avaliações Recebidas:** {len(avaliacoes_usuario)}")
        
        st.divider()
        st.subheader("Avaliações como Comodatário")
        st.write("Avaliações recebidas quando você pegou livros emprestados:")
        
        try:
            todas_avaliacoes = Views.avaliacao_listar()
            avaliacoes_como_comodatario = []
            
            for avaliacao in todas_avaliacoes:
                if avaliacao[0] != id_usuario:
                    try:
                        id_emprestimo = avaliacao[4]
                        emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                        solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                        id_solicitante = solicitacao[5]
                        
                        if id_solicitante == id_usuario:
                            avaliacoes_como_comodatario.append(avaliacao)
                    except:
                        continue
            
            if not avaliacoes_como_comodatario:
                st.info("Você ainda não recebeu nenhuma avaliação como comodatário.")
            else:
                dados_avaliacoes_comodatario = []
                for avaliacao in avaliacoes_como_comodatario:
                    dados = VisualizarPerfilUI._processar_avaliacao(avaliacao)
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
                
                # Tabela
                df_comodatario = pd.DataFrame(dados_avaliacoes_comodatario)
                st.dataframe(df_comodatario, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações como comodatário: {str(e)}")
        
        st.divider()
        st.subheader("Avaliações como Dono do Exemplar")
        st.write("Avaliações recebidas quando você emprestou seus exemplares:")
        
        try:
            todas_avaliacoes = Views.avaliacao_listar()
            avaliacoes_como_dono = []
            
            for avaliacao in todas_avaliacoes:
                if avaliacao[0] != id_usuario:
                    try:
                        id_emprestimo = avaliacao[4]
                        emprestimo = Views.emprestimo_listar_id(id_emprestimo)
                        solicitacao = Views.solicitacao_listar_id(emprestimo[1])
                        id_exemplar = solicitacao[4]
                        id_solicitante = solicitacao[5]
                        
                        meus_exemplares = Views.exemplar_listar_por_usuario(id_usuario)
                        if any(ex[0] == id_exemplar for ex in meus_exemplares):
                            avaliacoes_como_dono.append(avaliacao)
                    except:
                        continue
            
            if not avaliacoes_como_dono:
                st.info("Você ainda não recebeu nenhuma avaliação como dono de exemplar.")
            else:
                dados_avaliacoes_dono = []
                for avaliacao in avaliacoes_como_dono:
                    dados = VisualizarPerfilUI._processar_avaliacao(avaliacao)
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
            
        except Exception as e:
            st.error(f"Erro ao carregar avaliações como dono: {str(e)}")
        
        st.divider()
        st.subheader("Exemplares Disponíveis")
        
        exemplares_disponiveis = [e for e in exemplares if e[3] == 'disponivel']
        
        if not exemplares_disponiveis:
            st.info("Este usuário não tem exemplares disponíveis no momento.")
        else:
            for exemplar in exemplares_disponiveis:
                id_exemplar = exemplar[0]
                id_livro = exemplar[2]
                
                livro = Views.livro_listar_por_id(id_livro)
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{livro[1]}**")
                        st.write(f"Autor: {livro[2]}")
                        st.write(f"Cód. Exemplar: {id_exemplar}")
                    
                    with col2:
                        if "usuario_id" in st.session_state and st.session_state["usuario_id"] != id_usuario:
                            if st.button("Solicitar", key=f"solicitar_{id_exemplar}"):
                                st.session_state[f"solicitar_exemplar_{id_exemplar}"] = True
                        else:
                            st.write("Seu exemplar")
        
        # Formulários de solicitação (se existirem)
        for exemplar in exemplares_disponiveis:
            id_exemplar = exemplar[0]
            if st.session_state.get(f"solicitar_exemplar_{id_exemplar}"):
                VisualizarPerfilUI.form_solicitar_emprestimo(id_exemplar, id_usuario)
    
    @staticmethod
    def form_solicitar_emprestimo(id_exemplar, id_dono):
        """Formulário para solicitar empréstimo de um exemplar"""
        st.subheader("Solicitar Empréstimo")
        
        dias_emprestimo = st.number_input(
            "Quantos dias você precisa com o livro?", 
            min_value=1, 
            max_value=30, 
            value=7
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Confirmar Solicitação"):
                try:
                    Views.solicitacao_inserir(
                        st.session_state["usuario_id"], 
                        id_exemplar, 
                        dias_emprestimo
                    )
                    st.success("Solicitação enviada com sucesso! Aguarde a aprovação do dono.")
                    del st.session_state[f"solicitar_exemplar_{id_exemplar}"]
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao solicitar empréstimo: {str(e)}")
        
        with col2:
            if st.button("Cancelar"):
                del st.session_state[f"solicitar_exemplar_{id_exemplar}"]
                st.rerun()
