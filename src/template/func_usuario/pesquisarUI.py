import streamlit as st
import pandas as pd
from datetime import datetime
from views import Views
import time

class PesquisarUI:
    @staticmethod
    def main():
        st.header("Pesquisar Livros e Exemplares Disponíveis")
        
        livros = Views.livro_listar()
        
        if not livros:
             st.info("Nenhum livro cadastrado.")
             return

        df_livros = pd.DataFrame(livros, columns=['ID', 'Título', 'Autor', 'Páginas', 'ISBN', 'Capa'])
        
        termo = st.text_input("Digite o termo de pesquisa (título, autor):")
        
        if termo:
            mask = (
                df_livros['Título'].str.contains(termo, case=False) |
                df_livros['Autor'].str.contains(termo, case=False)
            )
            df_filtrado = df_livros[mask]
        else:
            df_filtrado = df_livros

        st.write("**Livros encontrados:**")
        
        if df_filtrado.empty:
            st.warning("Nenhum livro encontrado com este termo.")
            return
            
        for _, livro in df_filtrado.iterrows():
            id_livro = livro['ID']
            titulo_livro = livro['Título']
            autor_livro = livro['Autor']
            
            try:
                avaliacoes_livro = Views.avaliacao_calcular_media_por_livro(id_livro)
                media_livro = avaliacoes_livro['media_nota']
                total_livro = avaliacoes_livro['total_avaliacoes']
                
                if total_livro > 0:
                    estrelas_livro = "⭐" * round(media_livro)
                    avaliacao_livro_texto = f"{estrelas_livro} ({media_livro}/5) - {total_livro} avaliação(ões)"
                else:
                    avaliacao_livro_texto = "Sem avaliações gerais ainda"
            except:
                avaliacao_livro_texto = "Sem avaliações gerais ainda"
            
            with st.expander(f"**{titulo_livro}** - {autor_livro}", expanded=True):
                col_img, col_info = st.columns([1, 4])
                with col_img:
                    capa_url = livro.get('Capa') if isinstance(livro, dict) else livro['Capa'] if len(livro) > 5 else None
                    if capa_url:
                        try:
                            st.image(capa_url, width=120, caption=titulo_livro)
                        except Exception:
                            st.text("[Capa inválida]")
                    else:
                        st.text("[Sem capa]")

                with col_info:
                    st.info(f"**Avaliações Gerais do Livro:** {avaliacao_livro_texto}")
                
                exemplares = Views.exemplar_listar_por_livro(id_livro)
                
                exemplares_disponiveis = [ex for ex in exemplares if ex[3] == 'disponivel']
                
                if not exemplares_disponiveis:
                    st.warning("Nenhum exemplar disponível para este livro no momento.")
                else:
                    st.success(f"{len(exemplares_disponiveis)} exemplar(es) disponível(is):")
                    
                    for exemplar in exemplares_disponiveis:
                        id_exemplar = exemplar[0]
                        id_dono = exemplar[1]
                        
                        try:
                            dono_info = Views.usuario_listar_por_id(id_dono)
                            nome_dono = dono_info[1] if dono_info else "Usuário desconhecido"
                        except:
                            nome_dono = "Usuário desconhecido"
                        
                        try:
                            avaliacoes_exemplar = Views.avaliacao_calcular_media_por_exemplar(id_exemplar)
                            media_exemplar = avaliacoes_exemplar['media_nota']
                            total_exemplar = avaliacoes_exemplar['total_avaliacoes']
                            
                            if total_exemplar > 0:
                                estrelas_exemplar = "⭐" * round(media_exemplar)
                                avaliacao_exemplar_texto = f"{estrelas_exemplar} ({media_exemplar}/5) - {total_exemplar} avaliação(ões)"
                            else:
                                avaliacao_exemplar_texto = "Sem avaliações deste exemplar"
                        except:
                            avaliacao_exemplar_texto = "Sem avaliações deste exemplar"
                        
                        try:
                            avaliacoes_dono = Views.avaliacao_calcular_media_por_dono(id_dono)
                            media_dono = avaliacoes_dono['media_nota']
                            total_dono = avaliacoes_dono['total_avaliacoes']
                            
                            if total_dono > 0:
                                estrelas_dono = "⭐" * round(media_dono)
                                avaliacao_dono_texto = f"{estrelas_dono} ({media_dono}/5) - {total_dono} avaliação(ões)"
                            else:
                                avaliacao_dono_texto = "Sem avaliações do dono"
                        except:
                            avaliacao_dono_texto = "Sem avaliações do dono"
                        
                        with st.container(border=True):
                            st.markdown(f"**Cód. Exemplar:** {id_exemplar}")
                            st.markdown(f"**Dono:** {nome_dono}")
                            st.markdown("**🟢 Status:** Disponível para empréstimo")
                            
                            st.markdown("---")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Avaliações do Exemplar:**")
                                st.info(avaliacao_exemplar_texto)
                            
                            with col2:
                                st.markdown("**Avaliações do Dono:**")
                                st.success(avaliacao_dono_texto)
                            
                            st.markdown("---")
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.write("")
                            with col2:
                                if st.button("Solicitar", key=f"solicitar_{id_exemplar}", use_container_width=True):
                                    PesquisarUI.realizar_emprestimo(id_exemplar, titulo_livro, nome_dono)
                            with col3:
                                st.write("⏱️")
                                st.write("Até 30 dias")

    @staticmethod
    def realizar_emprestimo(id_exemplar, titulo_livro, nome_dono):
        """Método auxiliar para processar a solicitação de empréstimo"""
        # Verifica se existe usuário logado
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado para solicitar um empréstimo.")
            return

        id_usuario = st.session_state["usuario_id"]
        
        # Usar expander para o formulário
        with st.expander(f"📋 Solicitar Empréstimo - {titulo_livro}", expanded=True):
            st.write(f"**Livro:** {titulo_livro}")
            st.write(f"**Dono:** {nome_dono}")
            st.write(f"**Cód. Exemplar:** {id_exemplar}")
            
            dias_emprestimo = st.number_input(
                "Por quantos dias você precisa com o livro?", 
                min_value=1, 
                max_value=30, 
                value=7,
                key=f"dias_{id_exemplar}",
                help="O dono do exemplar precisará aprovar sua solicitação"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enviar Solicitação", key=f"enviar_{id_exemplar}", use_container_width=True):
                    try:
                        Views.solicitacao_inserir(id_usuario, id_exemplar, dias_emprestimo)
                        st.success("**Solicitação enviada com sucesso!**")
                        st.info("O dono do exemplar será notificado e poderá aprovar sua solicitação.")
                        time.sleep(3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao solicitar empréstimo: {str(e)}")
            with col2:
                if st.button("Cancelar", key=f"cancelar_{id_exemplar}", use_container_width=True):
                    st.rerun()