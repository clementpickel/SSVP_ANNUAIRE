import streamlit as st
from Service.annuaire_handler import AnnuaireHandler, cleanup
from UI.card import display_mail_card, display_phone_card, display_ids, display_name_card, display_adresse_card, display_fonctions_card, display_cd_card
from UI.header_selector import header_selector
import numpy as np

st.title("Annuaire SSVP")

# Initialize handler
sf = AnnuaireHandler()

def handle_params():
    params = st.query_params
    if params != None and "selectedoption" in params :
        if params["selected_option"] == "ID":
            if id in params and params["id"] != "":
                return "ID", {"id": params["id"][0]}
            else:
                return "ID", None
    return None, None
            



header_selector_option, params = handle_params()
header_selector_option, params = header_selector()

start = False
show_cd = False

if header_selector_option == "Email" and params["email"] != " ":
    email = params["email"]
    person_ids = sf.get_id(email)
    person_ids_sage = sf.get_id_sage(email)
    start = True

elif header_selector_option == "ID" and params["id"] != "":
    individuid = params["id"]
    person_ids = (individuid,)
    person_ids_sage = (individuid,)
    start = True

elif header_selector_option == "Nom Prénom" and params is not None and params["nom"] != "" and params["prenom"] != "":
    nom = params["nom"]
    prenom = params["prenom"]
    print(nom, prenom)
    person_ids = sf.get_pn_id_from_name(nom, prenom)
    person_ids_sage = sf.get_sage_id_from_name(nom, prenom)
    start = True

elif header_selector_option == "CD/CF" and params != None and "cd" in params and params["cd"] != " ":
    cd = params["cd"]
    cd_info = sf.get_persons_by_cd(cd)
    display_cd_card(cd_info)
    start = False

if start:   
    if person_ids is None:
        st.error("Aucun individu trouvé pour cet email dans PNDATA.")
        st.stop()

    if person_ids is None:
        st.error("Aucun individu trouvé pour cet email dans PNDATA.")
        st.stop()

    sage_info = sf.get_sage_info(person_ids_sage) if person_ids_sage else None
    if sage_info is not None:
        sage_info = sage_info.replace("30/12/1899", np.nan)

    pn_mail = sf.get_pn_email(person_ids) if person_ids else None
    pn_adresse = sf.get_pn_adresse(person_ids) if person_ids else None
    pn_phone = sf.get_pn_phone(person_ids) if person_ids else None
    pn_functions = cleanup(sf.get_person_functions_pn(person_ids) if person_ids else None)

    st.markdown("---")
    display_name_card(sage_info, pn_adresse)

    st.markdown("---")
    display_ids(person_ids_sage if person_ids_sage else None, person_ids if person_ids else None)

    st.markdown("---")
    display_mail_card(sage_info, pn_mail)

    st.markdown("---")
    display_phone_card(sage_info, pn_phone)

    st.markdown("---")
    display_adresse_card(sage_info, pn_adresse)

    st.markdown("---")
    display_fonctions_card(sage_info, pn_functions)
