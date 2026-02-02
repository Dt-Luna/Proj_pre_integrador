import streamlit as st
from views import Views
from datetime import datetime

class SolicitacaoUI:
    def main():
        st.title("Solicitações")
        tab1, tab2, tab3 = st.tabs({}) 