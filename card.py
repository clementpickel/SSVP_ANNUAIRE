import streamlit as st

def display_adresse_card(person_info: dict):
    # Header with full name
    st.header(f"{person_info.get('IDCIVILITE','')} {person_info.get('PRENOM','')} {person_info.get('NOM','')}")

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Adresse")
        st.text(f"{person_info.get('NUMVOIE','')} {person_info.get('LIBVOIE','')}")
        if person_info.get('COMPLEMENTADR','') and person_info.get('COMPLEMENTNOM',''):
            st.text(f"{person_info.get('COMPLEMENTADR','')} {person_info.get('COMPLEMENTNOM','')}")
        st.text(f"{person_info.get('CODEPOSTAL','')}")
        st.text(f"Acheminement: {person_info.get('ACHEMINEMENT','')}")
        st.text(f"Lieu-dit: {person_info.get('LIEUDITPOSTALOUBP','')}")
        st.text(f"Code Action: {person_info.get('CODEACTIONRECRUT','')}")

    with col2:
        # st.subheader("Téléphone")
        # if person_info.get('INDICATIFTEL',''):
        #     st.text(f"{person_info.get('INDICATIFTEL','')} {person_info.get('NUMTEL','')}")
        # else:
        #     st.text(f"{person_info.get('NUMTEL','')}")
        st.subheader("ID")
        st.text(f"{person_info.get('IDINDIVIDU','')}")


def display_telephone_card(person_info: dict):
    if person_info.get('INDICATIFTEL',''):
        st.text(f"{person_info.get('INDICATIFTEL','')} {person_info.get('NUMTEL','')}")
    else:
        st.text(f"{person_info.get('NUMTEL','')}")

