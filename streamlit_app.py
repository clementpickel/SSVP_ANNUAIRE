import streamlit as st
from annuaire_handler import AnnuaireHandler, cleanup
from card import display_telephone_card, display_adresse_card

st.title("Annuaire SSVP")

# Initialize handlera
sf = AnnuaireHandler()

@st.cache_data(ttl=3600)
def load_emails():
    return sf.get_emails()


emails = load_emails()
email = st.selectbox("Email:", options=emails)

show_active = st.checkbox("Montrer seulement les fonctions actuelles")

# st.text('ou')

# col1, col2 = st.columns(2)
# with col1:
#     name = st.text_input("Nom")
# with col2:
#     firstname = st.text_input("Prénom")

 

def handle_duplicate(df):
    doublon = len(df) - len(df.drop_duplicates())
    if doublon == 1:
        st.warning("1 doublon")
    elif doublon > 1:
        st.warning(f"{doublon} doublons")
    return df.drop_duplicates()

person_df = None
try:
    if email != " ":
        # Search by email
        person_df = sf.get_person_functions(email)
        address_df = sf.get_person_address(email)
        phones_df = sf.get_person_phones(email)

        st.markdown("---")
        if address_df.empty:
            st.warning("Pas d'adresse trouvé")
        else:
            if len(address_df) == 1:
                st.success(f"{len(address_df)} adresse trouvée")
            else:
                st.success(f"{len(address_df)} adresses trouvées")
            address_df = handle_duplicate(address_df)
            for _, row in address_df.iterrows():
                display_adresse_card(row.to_dict())

        st.markdown("---")
        if phones_df.empty:
            st.warning("Pas de téléphone trouvé")
        else:
            if len(phones_df) == 1:
                st.success(f"{len(phones_df)} téléphone trouvée")
            else:
                st.success(f"{len(phones_df)} téléphones trouvées")
            phones_df = handle_duplicate(phones_df)
            st.subheader("Téléphone")
            for _, row in phones_df.iterrows():
                display_telephone_card(row.to_dict())
            
        

    # elif name and firstname:
    #     st.write(name, firstname)
    #     # Search by name + firstname
    #     person_df = sf.get_person_functions_name(name, firstname)
    #     st.write(person_df)

    if person_df is not None:
        
        # Clean up the data
        person_df = cleanup(person_df, show_active)
        st.markdown("---")
        if person_df.empty:
            st.warning("No data found for this person.")
        else:
            st.success(f"Found {len(person_df)} records")
            person_df = handle_duplicate(person_df)
            st.subheader("Fonctions")
            st.table(person_df)

except Exception as e:
    st.error(f"Error: {e}")

finally:
    sf.close()