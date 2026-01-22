import streamlit as st
from views import Views
from datetime import datetime, date
import time

class PerfilUI:
    def main():
        st.header("Perfil do Usuário")

        # 1. Recuperar dados da sessão (agora salvos individualmente)
        id_usuario = st.session_state.get("usuario_id")
        username_atual = st.session_state.get("usuario_nome")
        email_atual = st.session_state.get("usuario_email")
        data_nascimento_atual = st.session_state.get("usuario_data_nascimento", "2000-01-01")

        # Se por acaso não tiver usuário logado, para a execução
        if not id_usuario:
            st.error("Nenhum usuário logado.")
            return

        # 2. Formulário de Edição
        # O valor inicial (value) vem da sessão
        novo_nome = st.text_input("Nome de usuário", value=username_atual)
        novo_email = st.text_input("E-mail", value=email_atual)
        nova_senha = st.text_input("Nova Senha (deixe em branco para manter)", type="password")
        
        try:
            data_obj = datetime.strptime(data_nascimento_atual, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            data_obj = date(2000, 1, 1)
        
        # Usar date_input com os limites apropriados
        data_nascimento_input = st.date_input(
            "Data de Nascimento",
            value=data_obj,
            min_value=date(1925, 1, 1),
            max_value=date.today()
        )
        data_nascimento = data_nascimento_input.strftime("%Y-%m-%d")

        if st.button("Atualizar Perfil"):
            try:
                # Se a senha estiver vazia, precisamos pegar a senha antiga do banco 
                # ou obrigar o usuário a digitar a senha atual.
                # Para simplificar este exemplo, se a senha for vazia, mantemos a senha anterior
                if nova_senha:
                    senha_para_salvar = nova_senha
                else:
                    st.warning("Por favor, informe a senha para atualizar o perfil.")
                    return

                # Chama a View para atualizar
                Views.usuario_atualizar(
                    id_usuario, 
                    novo_nome, 
                    senha_para_salvar, 
                    novo_email, 
                    data_nascimento
                )
                
                st.success("Perfil atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
                
                # Atualiza a sessão com os novos dados para refletir na hora
                st.session_state["usuario_nome"] = novo_nome
                st.session_state["usuario_email"] = novo_email
                st.session_state["usuario_data_nascimento"] = data_nascimento
                
                # Recarrega a página
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao atualizar perfil: {e}")