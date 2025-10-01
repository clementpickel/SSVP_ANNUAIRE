import streamlit as st
import pandas as pd

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


def _display_emails_from_df(df: pd.DataFrame, columns: list[str]):
    """Helper to display emails from given DataFrame and list of columns."""
    if df is None or df.empty or df[columns].dropna().empty:
        st.text("Aucun information trouvée.")
        return False
    
    for col in columns:
        if col in df.columns:
            for email in df[col].dropna():
                st.text(email)
    return True


def display_mail_card(person_info_sage: pd.DataFrame | None, person_info_pndata: pd.DataFrame | None):
    st.subheader("Email")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Emails Sage")
        _display_emails_from_df(person_info_sage, ["EMAIL1", "EMAIL2"])

    with col2:
        st.markdown("##### Emails PNData")

        has_pndata = _display_emails_from_df(person_info_pndata, ["ADRMAIL"])
        if not has_pndata:
            st.text("Aucun email trouvé dans PNDATA.")

def display_phone_card(person_info_sage: pd.DataFrame | None, person_info_pndata: pd.DataFrame | None):
    st.subheader("Téléphone")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Téléphone Sage")
        _display_emails_from_df(person_info_sage, ["TELEPHONE1", "TELEPHONE2"])

    with col2:
        st.markdown("##### Téléphone PNData")
        _display_emails_from_df(person_info_pndata, ["INDICATIFTEL", "NUMTEL"])

def display_ids(sage_id: list[str], pndata_id: list[str]):
    st.subheader("ID")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### ID Sage")
        if sage_id is None or len(sage_id) == 0:
            st.text("Aucun ID Sage trouvé.")
        else:
            for id in sage_id:
                st.text(id)

    with col2:
        st.markdown("##### ID PNData")
        if pndata_id is None or len(pndata_id) == 0:
            st.text("Aucun ID Sage trouvé.")
        else:
            for id in pndata_id:
                st.text(id)

def display_name_card(sage_info: pd.DataFrame | None, pndata_info: pd.DataFrame | None):
    st.subheader("Nom Prénom")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Nom Prénom Sage")
        if sage_info is None or sage_info.empty:
            st.text("Aucun Nom Prénom trouvé.")
        else:
            for _, row in sage_info.iterrows():
                st.text(f"{row.get('PRENOM','')} {row.get('NOM','')}")

    with col2:
        st.markdown("##### Nom Prénom PNData")
        if pndata_info is None or pndata_info.empty:
            st.text("Aucun Nom Prénom trouvé.")
        else:
            for _, row in pndata_info.iterrows():
                st.text(f"{row.get('PRENOM','')} {row.get('NOM','')}")

def display_adresse_card(sage_info: pd.DataFrame | None, pndata_info: pd.DataFrame | None):
    st.subheader("Adresse")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Adresse Sage")
        if sage_info is None or sage_info.empty:
            st.text("Aucune adresse trouvée.")
        else:
            for _, row in sage_info.iterrows():
                if row.get("ADRESS1"):
                    st.text(row["ADRESS1"])
                if row.get("ADRESS2"):
                    st.text(row["ADRESS2"])
                if row.get("ADRESS3"):
                    st.text(row["ADRESS3"])
                if row.get("ADRESS4"):
                    st.text(row["ADRESS4"])

                st.text(f"Code postale: {row.get('CODEPOSTAL','')}")
                st.text(f"Ville: {row.get('VILLE','')}")
                st.text(f"Pays: {row.get('CODEDUPAYS','')}")

    with col2:
        st.markdown("##### Adresse PNData")
        if pndata_info is None or pndata_info.empty:
            st.text("Aucune adresse trouvée.")
        else:
            for _, row in pndata_info.iterrows():
                st.text(f"{row.get('NUMVOIE','')} {row.get('LIBVOIE','')}")
                if row.get('COMPLEMENTADR','') and row.get('COMPLEMENTNOM',''):
                    st.text(f"{row.get('COMPLEMENTADR','')} {row.get('COMPLEMENTNOM','')}")
                st.text(f"{row.get('CODEPOSTAL','')}")
                st.text(f"Acheminement: {row.get('ACHEMINEMENT','')}")

                if row.get("LIEUDITPOSTALOUBP"):
                    st.text(f"Lieu-dit: {row.get('LIEUDITPOSTALOUBP','')}")
                if row.get("CODEACTIONRECRUT"):
                    st.text(f"Code Action: {row.get('CODEACTIONRECRUT','')}")

def get_date_string(date: pd.Timestamp) -> str:
    if pd.isna(date) or date == "":
        return "Aujourd'hui"
    if isinstance(date, pd.Timestamp):
        return date.strftime('%d/%m/%Y')
    return str(date)

def display_fonctions_card(sage_info: pd.DataFrame | None, pndata_info: pd.DataFrame | None):
    st.subheader("Fonctions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Fonctions Sage")
        if sage_info is None or sage_info.empty:
            st.text("Aucune fonction trouvée.")
        else:
            for _, row in sage_info.iterrows():
                for i in ["", "2", "3", "4", "5"]:
                    if row.get(f'FONCTION{i}',''):
                        st.text(f"{row.get(f'FONCTION{i}','')} - {row.get(f'ENTITEAPPARTENANCE{i}','')}")
                        st.text(f"{get_date_string(row.get(f'DATEFONCTION{i}',''))} - {get_date_string(row.get(f'DATEFINFONCTION{i}',''))}")
                        st.markdown("---")

    with col2:
        st.markdown("##### Fonctions PNData")
        if pndata_info is None or pndata_info.empty:
            st.text("Aucune fonction trouvée.")
        else:
            for _, row in pndata_info.iterrows():
                st.text(f"{row.get('LIBELLE_LIEN','')} - {row.get('LIB_TYPELIEN','')}")
                st.text(f"{row.get('LIBELLEENTITE','')}")
                st.text(f"{get_date_string(row.get('DATE_TEMP_DEBUT',''))} - {get_date_string(row.get('DATE_TEMP_FIN',''))}")
                if row.get('DATEANNULATION',''):
                    st.text(f"  (Annulé le {get_date_string(row.get('DATEANNULATION',''))}")
                st.markdown("---")


def display_cd_card(cd_info: pd.DataFrame):
    df_sorted = cd_info.sort_values(by="FONCTION")
    df_sorted = df_sorted.replace("30/12/1899", pd.NA)
    # df_sorted["IDENTIFIANTCONTACTPN"] = df_sorted["IDENTIFIANTCONTACTPN"].astype(int)
    st.subheader("Informations CD/CF")
    if df_sorted is None or cd_info.empty:
        st.text("Aucune information trouvée.")
    else:
        st.dataframe(df_sorted)
        for row in df_sorted.itertuples():
            st.markdown(f"**{row.NOM} {row.PRENOM}**")
            st.text(f"ID: {int(row.IDENTIFIANTCONTACTPN) if pd.notna(row.IDENTIFIANTCONTACTPN) else 'Non renseigné'}")
            st.text(f"Fonction: {row.FONCTION}")
            st.text(f"Date de début: {row.DATEFONCTION} --- {row.DATEFINFONCTION}")
            st.text(f"Téléphone: {row.TELEPHONE1} --- {row.TELEPHONE2}")
            st.text(f"Email: {row.EMAIL1} {row.EMAIL2 if row.EMAIL2 else ''}")
            st.text(f"Adresse: {row.ADRESS1 if row.ADRESS1 else ''} {row.ADRESS2} {row.ADRESS3} {row.ADRESS4} {row.CODEPOSTAL} {row.VILLE} {row.CODEDUPAYS}")
            if pd.notna(row.IDENTIFIANTCONTACTPN):
                if st.button("Search by ID", key=f"search_{row.IDENTIFIANTCONTACTPN}"):
                    st.experimental_set_query_params(selectedoption="ID", id=int(row.IDENTIFIANTCONTACTPN)) # deprecated
                    # st.query_params.clear()
                    # st.query_params.from_dict({
                    #     "selectedoption": "ID",
                    #     "id": str(int(row.IDENTIFIANTCONTACTPN))
                    # })
            st.markdown("---")

def display_fonctions_card_entite(info_df: pd.DataFrame):
    info_df["IDREF_LIEN"] = info_df["IDREF_LIEN"].astype(int)
    info_df["DATEANNULATION"] = info_df["DATEANNULATION"].replace("00000000000000000", pd.NA)
    info_df["DATEANNULATION"] = pd.to_datetime(
        info_df["DATEANNULATION"].str.slice(0, 8),
        format="%Y%m%d",
        errors="coerce"
    )
    info_df = info_df.dropna(subset=["NOM", "PRENOM"])

    # Merge emails and tel
    info_df = (
        info_df.groupby(
            ["NOM", "PRENOM", "LIBELLE_LIEN", "LIB_TYPELIEN", "IDREF_LIEN", "DATEANNULATION"],
            dropna=False
        )
        .agg({
            "ADRMAIL": lambda x: ", ".join(sorted(set(x.dropna()))),
            "INDICATIFTEL": lambda x: ", ".join(sorted(set(x.dropna().astype(str)))),
            "NUMTEL": lambda x: ", ".join(sorted(set(x.dropna().astype(str))))
        })
        .reset_index()
    )
    info_df = info_df.sort_values(by="IDREF_LIEN")

    show_active = st.checkbox("Afficher uniquement les fonctions actives", value=True)
    if show_active:
        info_df = info_df[(info_df["DATEANNULATION"].isna()) | (info_df["DATEANNULATION"] >= pd.Timestamp.today())]

    st.dataframe(info_df, use_container_width=True)
    for i, row in info_df.iterrows():
        st.write(f"**{row['LIBELLE_LIEN']}** - {row['PRENOM']} - {row['NOM']} - {row['LIB_TYPELIEN']}")
        
        if st.button("Plus d'informations)", key=f"btn_{i}"):
            st.write(f"Number: {row['NUMTEL']}")
            st.write(f"Email: {row['ADRMAIL']}")
                