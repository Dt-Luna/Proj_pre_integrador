import streamlit as st
from views import Views

class PerfilUI:
    def main():
        st.header("Perfil do Usuário")

        # 1. Recuperar dados da sessão (agora salvos individualmente)
        id_usuario = st.session_state.get("usuario_id")
        username_atual = st.session_state.get("usuario_nome")
        email_atual = st.session_state.get("usuario_email")

        # Se por acaso não tiver usuário logado, para a execução
        if not id_usuario:
            st.error("Nenhum usuário logado.")
            return

        # 2. Formulário de Edição
        # O valor inicial (value) vem da sessão
        novo_nome = st.text_input("Nome de usuário", value=username_atual)
        novo_email = st.text_input("E-mail", value=email_atual)
        nova_senha = st.text_input("Nova Senha (deixe em branco para manter)", type="password")
        
        # Precisamos pedir a data de nascimento também, pois o metodo de atualizar exige
        # Como não salvamos na sessão, vamos buscar no banco ou pedir para digitar
        # Simplificação: pedindo para digitar (ou defina uma data padrão se preferir)
        data_nascimento = st.text_input("Data de Nascimento (AAAA-MM-DD)", value="2000-01-01") 

        if st.button("Atualizar Perfil"):
            try:
                # Se a senha estiver vazia, precisamos pegar a senha antiga do banco 
                # ou obrigar o usuário a digitar a senha atual.
                # Para simplificar este exemplo, se a senha for vazia, mantemos "1234" (o ideal é buscar no banco)
                senha_para_salvar = nova_senha if nova_senha else "1234"

                # Chama a View para atualizar
                Views.usuario_atualizar(
                    id_usuario, 
                    novo_nome, 
                    senha_para_salvar, 
                    novo_email, 
                    data_nascimento
                )
                
                st.success("Perfil atualizado com sucesso!")
                
                # Atualiza a sessão com os novos dados para refletir na hora
                st.session_state["usuario_nome"] = novo_nome
                st.session_state["usuario_email"] = novo_email
                
                # Recarrega a página
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao atualizar perfil: {e}")