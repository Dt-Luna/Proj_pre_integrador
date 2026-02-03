import streamlit as st
from views import Views
import pandas as pd
import time

class BibliotecaUI:
    def main():
        st.title("Minha Biblioteca Pessoal")
        st.markdown("Gerencie os exemplares de livros que você possui e compartilha com a comunidade.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Meus Exemplares", "Adicionar Exemplar", "Gerenciar Status", "Remover Exemplar"])
        with tab1: BibliotecaUI.ver_exemplares()
        with tab2: BibliotecaUI.adicionar_exemplar()
        with tab3: BibliotecaUI.gerenciar_status()
        with tab4: BibliotecaUI.excluir_exemplar()

    def ver_exemplares():
        st.subheader("Meus Exemplares Cadastrados")
        
        try:
            user_exemplares = Views.exemplar_listar_por_usuario(st.session_state.get("usuario_id"))
            
            if not user_exemplares:
                st.info("Você ainda não possui exemplares cadastrados.")
            else:
                # Criar DataFrame com informações mais detalhadas
                dados_exemplares = []
                for exemplar in user_exemplares:
                    id_exemplar = exemplar[0]
                    id_livro = exemplar[2]
                    status = exemplar[3]
                    
                    # Obter informações do livro
                    try:
                        livro_info = Views.livro_listar_por_id(id_livro)
                        if livro_info:
                            titulo_livro = livro_info[1]
                            autor_livro = livro_info[2]
                        else:
                            titulo_livro = "Livro desconhecido"
                            autor_livro = "Desconhecido"
                    except:
                        titulo_livro = "Livro desconhecido"
                        autor_livro = "Desconhecido"
                    
                    # Formatar status
                    status_icon = "🟢" if status == "disponivel" else "🔴" if status == "emprestado" else "⚠️"
                    status_text = status.replace("disponivel", "Disponível").replace("emprestado", "Emprestado")
                    
                    dados_exemplares.append({
                        'Cód. Exemplar': id_exemplar,
                        'Livro': titulo_livro,
                        'Autor': autor_livro,
                        'Status': f"{status_icon} {status_text}"
                    })
                
                df = pd.DataFrame(dados_exemplares)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Estatísticas
                total = len(user_exemplares)
                disponiveis = len([ex for ex in user_exemplares if ex[3] == 'disponivel'])
                emprestados = len([ex for ex in user_exemplares if ex[3] == 'emprestado'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Exemplares", total)
                with col2:
                    st.metric("🟢 Disponíveis", disponiveis)
                with col3:
                    st.metric("🔴 Emprestados", emprestados)

        except Exception as e:
            st.error(f"Erro ao listar exemplares: {e}")

    def adicionar_exemplar():
        st.subheader("Adicionar Novo Exemplar")
        
        livros = Views.livro_listar()      
        
        if not livros:
            st.warning("Nenhum livro modelo cadastrado no sistema.")
            return
        
        # Obter informações do usuário
        id_usuario = st.session_state.get("usuario_id")
        usuario_info = Views.usuario_listar_por_id(id_usuario)
        nome_usuario = usuario_info[1] if usuario_info else "Usuário"
        
        st.write(f"**Adicionando exemplar para:** {nome_usuario}")
        
        # Seleção do livro
        livros_opcoes = [(f"{livro[1]} - {livro[2]}", livro[0]) for livro in livros]
        livro_selecionado = st.selectbox("Selecione o livro:", livros_opcoes)
        id_livro = livro_selecionado[1]
        
        # Mostrar informações do livro selecionado
        livro_info = Views.livro_listar_por_id(id_livro)
        if livro_info:
            with st.container(border=True):
                st.write(f"**Título:** {livro_info[1]}")
                st.write(f"**Autor:** {livro_info[2]}")
                st.write(f"**Páginas:** {livro_info[3]}")
                st.write(f"**ISBN:** {livro_info[4]}")
        
        if st.button("Adicionar à Minha Biblioteca", use_container_width=True, type="primary"):
            try:
                Views.exemplar_inserir(id_usuario, id_livro)
                st.success("**Exemplar adicionado com sucesso!**")
                st.info("Seu exemplar agora está disponível para outros usuários encontrarem e solicitarem empréstimo.")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao adicionar exemplar: {e}")

    def gerenciar_status():
        st.subheader("Gerenciar Status dos Exemplares")
        st.markdown("Atualize o status dos seus exemplares quando eles forem emprestados ou devolvidos.")
        
        try:
            exemplares = Views.exemplar_listar_por_usuario(st.session_state.get('usuario_id'))
            
            if not exemplares:
                st.info("Você não possui exemplares para gerenciar.")
                return
            
            # Preparar opções para seleção
            opcoes_exemplares = []
            for exemplar in exemplares:
                id_exemplar = exemplar[0]
                id_livro = exemplar[2]
                status_atual = exemplar[3]
                
                # Obter título do livro
                try:
                    livro_info = Views.livro_listar_por_id(id_livro)
                    titulo_livro = livro_info[1] if livro_info else "Livro desconhecido"
                except:
                    titulo_livro = "Livro desconhecido"
                
                status_icon = "🟢" if status_atual == "disponivel" else "🔴"
                opcoes_exemplares.append((f"{status_icon} {titulo_livro} (Cód: {id_exemplar})", exemplar))
            
            if opcoes_exemplares:
                exemplar_selecionado = st.selectbox("📚 Selecione o exemplar:", opcoes_exemplares)
                exemplar = exemplar_selecionado[1]
                
                # Mostrar informações atuais
                with st.container(border=True):
                    st.write(f"**Cód. Exemplar:** {exemplar[0]}")
                    st.write(f"**Status Atual:** {exemplar[3]}")
                
                # Novo status
                status_opcoes = ['disponivel', 'emprestado']
                status_labels = {
                    'disponivel': '🟢 Disponível para empréstimo',
                    'emprestado': '🔴 Emprestado'
                }
                
                novo_status = st.selectbox(
                    "Novo status:",
                    status_opcoes,
                    format_func=lambda x: status_labels[x]
                )
                
                if st.button("Atualizar Status", use_container_width=True):
                    try:
                        Views.exemplar_atualizar(exemplar[0], exemplar[1], exemplar[2], novo_status)
                        st.success("**Status atualizado com sucesso!**")
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f'Erro ao atualizar exemplar: {e}')
        
        except Exception as e:
            st.error(f"Erro ao carregar exemplares: {e}")

    def excluir_exemplar():
        st.subheader("Remover Exemplar")
        st.warning("**Atenção:** Esta ação não pode ser desfeita!")
        
        try:
            exemplares = Views.exemplar_listar_por_usuario(st.session_state.get("usuario_id"))
            
            if not exemplares:
                st.info("Você não possui exemplares para remover.")
                return
            
            # Preparar opções para seleção
            opcoes_exemplares = []
            for exemplar in exemplares:
                id_exemplar = exemplar[0]
                id_livro = exemplar[2]
                status_atual = exemplar[3]
                
                # Obter título do livro
                try:
                    livro_info = Views.livro_listar_por_id(id_livro)
                    titulo_livro = livro_info[1] if livro_info else "Livro desconhecido"
                except:
                    titulo_livro = "Livro desconhecido"
                
                # Não permitir excluir exemplares emprestados
                if status_atual == 'emprestado':
                    continue
                    
                status_icon = "🟢" if status_atual == "disponivel" else "⚠️"
                opcoes_exemplares.append((f"{status_icon} {titulo_livro} (Cód: {id_exemplar})", exemplar))
            
            if not opcoes_exemplares:
                st.warning("Você não possui exemplares disponíveis para remover (apenas exemplares não emprestados podem ser removidos).")
                return
            
            exemplar_selecionado = st.selectbox("Selecione o exemplar para remover:", opcoes_exemplares)
            exemplar = exemplar_selecionado[1]
            
            # Confirmação
            with st.container(border=True):
                st.write(f"**Tem certeza que deseja remover este exemplar?**")
                st.write(f"**Cód. Exemplar:** {exemplar[0]}")
                st.write(f"**Status:** {exemplar[3]}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirmar Remoção", use_container_width=True, type="secondary"):
                    try:
                        Views.exemplar_excluir(exemplar[0])
                        st.success("**Exemplar removido com sucesso!**")
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir exemplar: {e}")
            with col2:
                if st.button("Cancelar", use_container_width=True):
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Erro ao carregar exemplares: {e}")
