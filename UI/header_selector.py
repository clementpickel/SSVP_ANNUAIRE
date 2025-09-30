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
        return selected_option, {"email": email}

    elif selected_option == "ID":
        individuid = st.text_input("ID :")
        if id != "":
            return selected_option, {"id": individuid}

    elif selected_option == "Nom Prénom":
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom :")
        with col2:
            prenom = st.text_input("Prénom :")
        if nom != "" and prenom != "":
            return selected_option, {"nom": nom, "prenom": prenom}

    elif selected_option == "Téléphone":
        st.warning("Recherche par Téléphone non implémentée")
        st.stop()

    return selected_option, None
