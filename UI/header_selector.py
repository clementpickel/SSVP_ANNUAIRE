import streamlit as st
from Service.annuaire_handler import AnnuaireHandler

sf = AnnuaireHandler()

@st.cache_data(ttl=3600)
def load_emails():
    return sf.get_emails()

@st.cache_data(ttl=3600)
def load_cd():
    return sf.get_cd()

def header_selector():
    with st.container():
        _, main, _ = st.columns([1,2,1])
        with main:
            options = ["Email", "Nom Prénom", "ID", "Téléphone", "CD/CF", "CD/CF bis"]
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
            
            elif selected_option == "CD/CF":
                cds = sf.get_cd()
                cd = st.selectbox("CD/CF :", options=cds)
                if cd != " ":
                    return selected_option, {"cd": cd}
            
            elif selected_option == "CD/CF bis":
                options = ["CD", "CF", "AS", "CL", "AD", "ZD", "ZF", "ZL"]
                types = st.selectbox("Type: ", options=options)
                dept = st.text_input("Département: ")

                if dept != "":
                    dept_options = sf.get_entites_by_type_and_dept(types, dept)
                    if len(dept_options) == 0:
                        st.warning("Aucune entité trouvée pour ce type et département.")
                        st.stop()
                        return None, None
                    elif len(dept_options) == 1:
                        selected_entite = dept_options.iloc[0]
                        st.success(f"Entité trouvée: {selected_entite['LIBELLEENTITE']} ({selected_entite['IDINDIVIDU']})")
                        return selected_option, {"entite_id": selected_entite['IDINDIVIDU']}
                    else:
                        entite_option = list(zip(dept_options['IDENTITE'] + ' - ' + dept_options['LIBELLEENTITE'], dept_options['IDINDIVIDU']))
                        entite = st.selectbox("Plusieurs entités trouvées, veuillez en sélectionner une:", entite_option, format_func=lambda x: x[0])
                        _, value = entite
                        return selected_option, {"entite_id": value}

            return selected_option, None
