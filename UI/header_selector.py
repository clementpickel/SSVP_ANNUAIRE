import streamlit as st
from Service.annuaire_handler import AnnuaireHandler

sf = AnnuaireHandler()

@st.cache_data(ttl=3600)
def load_emails():
    return sf.get_emails()

def header_selector():
    options = ["Email", "Nom Prénom", "ID", "Téléphone"]
    selected_option = st.selectbox("Choisissez un champ :", options)

    if selected_option == "Email":
        emails = load_emails()
        email = st.selectbox("Email :", options=emails)
        show_active = st.checkbox("Montrer seulement les fonctions actuelles")
        return selected_option, {"email": email, "show_active": show_active}

    elif selected_option == "ID":
        st.warning("Recherche par ID non implémentée")
        st.stop()

    elif selected_option == "Nom Prénom":
        st.warning("Recherche par Nom Prénom non implémentée")
        st.stop()

    elif selected_option == "Téléphone":
        st.warning("Recherche par Téléphone non implémentée")
        st.stop()

    return selected_option, None
