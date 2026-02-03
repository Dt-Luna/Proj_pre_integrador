import streamlit as st
from views import Views
import pandas as pd
import time

class VisualizarPerfilUI:
    def main():
        st.title("👥 Visualizar Perfil de Usuário")
        
        # Campo para buscar usuário por email ou username
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
    
    def exibir_perfil(usuario):
        """Exibe informações do perfil de um usuário"""
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
        st.subheader("Exemplares Disponíveis")
        
        exemplares_disponiveis = [e for e in exemplares if e[3] == 'disponivel']
        
        if not exemplares_disponiveis:
            st.info("Este usuário não tem exemplares disponíveis no momento.")
        else:
            for exemplar in exemplares_disponiveis:
                id_exemplar = exemplar[0]
                id_livro = exemplar[2]
                
                # Obter detalhes do livro
                livro = Views.livro_listar_por_id(id_livro)
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{livro[1]}**")
                        st.write(f"Autor: {livro[2]}")
                        st.write(f"Cód. Exemplar: {id_exemplar}")
                    
                    with col2:
                        # Botão para solicitar empréstimo (se não for o próprio usuário)
                        if "usuario_id" in st.session_state and st.session_state["usuario_id"] != id_usuario:
                            if st.button("Solicitar", key=f"solicitar_{id_exemplar}"):
                                st.session_state[f"solicitar_exemplar_{id_exemplar}"] = True
                        else:
                            st.write("Seu exemplar")
        
        # Avaliações do usuário
        st.divider()
        st.subheader("Avaliações Recebidas")
        
        if not avaliacoes_usuario:
            st.info("Este usuário ainda não recebeu avaliações.")
        else:
            for avaliacao in avaliacoes_usuario:
                nota = avaliacao[3]
                comentario = avaliacao[4]
                id_emprestimo = avaliacao[5]
                
                avaliador_info = Views.usuario_listar_por_id(avaliacao[1])
                nome_avaliador = avaliador_info[1] if avaliador_info else "Anônimo"
                
                with st.container(border=True):
                    st.write(f"**Avaliador:** {nome_avaliador}")
                    st.write(f"**Nota:** {'⭐' * nota}")
                    if comentario:
                        st.write(f"**Comentário:** {comentario}")
        
        for exemplar in exemplares_disponiveis:
            id_exemplar = exemplar[0]
            if st.session_state.get(f"solicitar_exemplar_{id_exemplar}"):
                VisualizarPerfilUI.form_solicitar_emprestimo(id_exemplar, id_usuario)
    
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
