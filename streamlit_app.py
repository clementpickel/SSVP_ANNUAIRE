import streamlit as st
from Service.annuaire_handler import AnnuaireHandler, cleanup
from UI.card import display_mail_card, display_phone_card, display_ids, display_name_card, display_adresse_card, display_fonctions_card
from UI.header_selector import header_selector
import numpy as np

st.title("Annuaire SSVP")

# Initialize handlera
sf = AnnuaireHandler()

header_selector_option, params = header_selector()

has_pn_id = False
has_sage_id = False

if params != None and params["email"] != " ":
    email = params["email"]
    person_ids = sf.get_id(email)
    person_ids_sage = sf.get_id_sage(email)
    if person_ids is None:
        st.error("Aucun individu trouvé pour cet email dans PNDATA.")
        st.stop()
    else:
        has_pn_id = True

    if person_ids is None:
        st.error("Aucun individu trouvé pour cet email dans PNDATA.")
        st.stop()
    else:
        has_sage_id = True

    sage_info = sf.get_sage_info(person_ids_sage) if has_sage_id else None
    if sage_info is not None:
        sage_info = sage_info.replace("30/12/1899", np.nan)

    pn_mail = sf.get_pn_email(person_ids) if has_pn_id else None
    pn_adresse = sf.get_pn_adresse(person_ids) if has_pn_id else None
    pn_phone = sf.get_pn_phone(person_ids) if has_pn_id else None
    pn_functions = cleanup(sf.get_person_functions_pn(person_ids) if has_pn_id else None)

    st.markdown("---")
    display_name_card(sage_info, pn_adresse)

    st.markdown("---")
    display_ids(person_ids_sage if has_sage_id else None, person_ids if has_pn_id else None)

    st.markdown("---")
    display_mail_card(sage_info, pn_mail)

    st.markdown("---")
    display_phone_card(sage_info, pn_phone)

    st.markdown("---")
    display_adresse_card(sage_info, pn_adresse)

    st.markdown("---")
    display_fonctions_card(sage_info, pn_functions)
