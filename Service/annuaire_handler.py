import snowflake.connector
import pandas as pd
import os
import streamlit as st

# for local testing
# import dotenv 
# dotenv.load_dotenv()

class AnnuaireHandler:
    def __init__(self):
        self.conn = st.connection("snowflake")
        self.cur = self.conn.cursor()

    def tuple_to_str(self, t: tuple) -> str:
        return "(" + ", ".join(str(item) for item in t) + ")"

    def get_id(self, email: str):
        self.cur.execute(
            "SELECT IDINDIVIDU FROM ADRESSEEMAIL WHERE LOWER(ADRMAIL) = LOWER(?)",
            (email,)
        )
        result = self.cur.fetchone()
        return result if result else None

    def get_id_sage(self, email: str):
        self.cur.execute("""
            SELECT IDENTIFIANTCONTACTPN
            FROM BENEVOLES_SAGE
            WHERE LOWER(EMAIL1) = LOWER(?)
            OR LOWER(EMAIL2) = LOWER(?)
        """,
            (email, email)
        )
        result = self.cur.fetchone()
        return result if result else None

    def get_pn_id_from_name(self, nom: str, prenom: str):
        self.cur.execute(
            "SELECT IDINDIVIDU FROM INDIVIDUADRESSE WHERE LOWER(NOM) = LOWER(?) AND LOWER(PRENOM) = LOWER(?)",
            (nom, prenom)
        )
        result = self.cur.fetchone()
        return result if result else None

    def get_sage_id_from_name(self, nom: str, prenom: str):
        self.cur.execute(
            "SELECT IDENTIFIANTCONTACTPN FROM BENEVOLES_SAGE WHERE LOWER(NOM) = LOWER(?) AND LOWER(PRENOM) = LOWER(?)",
            (nom, prenom)
        )
        result = self.cur.fetchone()
        return result if result else None
    
    def get_sage_info(self, person_ids: tuple[int]):
        if not person_ids:
            return None
        query = f"""
            SELECT
                bs.*,
                er1.LIBELLEENTITE AS LIBELLEENTITE,
                er2.LIBELLEENTITE AS LIBELLEENTITE2,
                er3.LIBELLEENTITE AS LIBELLEENTITE3,
                er4.LIBELLEENTITE AS LIBELLEENTITE4,
                er5.LIBELLEENTITE AS LIBELLEENTITE5,

                rl1.LIBELLE_LIEN AS LIBELLE_LIEN,
                rl2.LIBELLE_LIEN AS LIBELLE_LIEN2,
                rl3.LIBELLE_LIEN AS LIBELLE_LIEN3,
                rl4.LIBELLE_LIEN AS LIBELLE_LIEN4,
                rl5.LIBELLE_LIEN AS LIBELLE_LIEN5,

                rt1.LIB_TYPELIEN as LIB_TYPELIEN,
                rt2.LIB_TYPELIEN as LIB_TYPELIEN2,
                rt3.LIB_TYPELIEN as LIB_TYPELIEN3,
                rt4.LIB_TYPELIEN as LIB_TYPELIEN4,
                rt5.LIB_TYPELIEN as LIB_TYPELIEN5


            FROM BENEVOLES_SAGE AS bs
            LEFT JOIN ENTITE_RESEAU AS er1 ON er1.IDINDIVIDU = bs.IDCONTACTENTITE
            LEFT JOIN ENTITE_RESEAU AS er2 ON er2.IDINDIVIDU = bs.IDCONTACTENTITE2
            LEFT JOIN ENTITE_RESEAU AS er3 ON er3.IDINDIVIDU = bs.IDCONTACTENTITE3
            LEFT JOIN ENTITE_RESEAU AS er4 ON er4.IDINDIVIDU = bs.IDCONTACTENTITE4
            LEFT JOIN ENTITE_RESEAU AS er5 ON er5.IDINDIVIDU = bs.IDCONTACTENTITE5

            LEFT JOIN REF_LIEN AS rl1 ON rl1.IDREF_LIEN = bs.FONCTION
            LEFT JOIN REF_LIEN AS rl2 ON rl2.IDREF_LIEN = bs.FONCTION2
            LEFT JOIN REF_LIEN AS rl3 ON rl3.IDREF_LIEN = bs.FONCTION3
            LEFT JOIN REF_LIEN AS rl4 ON rl4.IDREF_LIEN = bs.FONCTION4
            LEFT JOIN REF_LIEN AS rl5 ON rl5.IDREF_LIEN = bs.FONCTION5

            LEFT JOIN REF_TYPELIEN AS rt1 ON rt1.IDREF_TYPELIEN = bs.ENTITEAPPARTENANCE
            LEFT JOIN REF_TYPELIEN AS rt2 ON rt2.IDREF_TYPELIEN = bs.ENTITEAPPARTENANCE2
            LEFT JOIN REF_TYPELIEN AS rt3 ON rt3.IDREF_TYPELIEN = bs.ENTITEAPPARTENANCE3
            LEFT JOIN REF_TYPELIEN AS rt4 ON rt4.IDREF_TYPELIEN = bs.ENTITEAPPARTENANCE4
            LEFT JOIN REF_TYPELIEN AS rt5 ON rt5.IDREF_TYPELIEN = bs.ENTITEAPPARTENANCE5

            WHERE bs.IDENTIFIANTCONTACTPN IN {self.tuple_to_str(person_ids)};"""
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_pn_email(self, person_ids: tuple[int]):
        if not person_ids:
            return None
        query = f"SELECT ADRMAIL FROM ADRESSEEMAIL WHERE IDINDIVIDU IN {self.tuple_to_str(person_ids)}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_pn_phone(self, person_ids: tuple[int]):
        if not person_ids:
            return None
        query = f"SELECT INDICATIFTEL, NUMTEL, DATEANNULATION FROM TELEPHONE WHERE IDINDIVIDU IN {self.tuple_to_str(person_ids)}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        df = pd.DataFrame(data, columns=cols)
        df["DATEANNULATION"] = pd.to_datetime(df["DATEANNULATION"].astype(str), format="%Y%m%d%H%M%S%f", errors="coerce")
        today = pd.Timestamp.now().normalize()
        print(df)
        df = df[(df["DATEANNULATION"].isna()) | (df["DATEANNULATION"] >= today)]
        print(df)
        return df

    def get_pn_adresse(self, person_ids: tuple[int]):
        if not person_ids:
            return None
        query = f"""
        SELECT 
                CIVILITE, IDCIVILITE, ACHEMINEMENT, CODEPOSTAL, COMPLEMENTADR,
                COMPLEMENTNOM, LIBVOIE, LIEUDITPOSTALOUBP, NOM, NUMVOIE,
                PRENOM, CODEACTIONRECRUT, IDINDIVIDU
            FROM INDIVIDUADRESSE 
            WHERE IDINDIVIDU IN {self.tuple_to_str(person_ids)}
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)
    
    def get_person_functions_pn(self, person_ids: tuple[int]):
        if not person_ids:
            return None
        query = f"""
            SELECT 
                rl.LIBELLE_LIEN,
                rt.LIB_TYPELIEN,
                er.LIBELLEENTITE,
                l.DATE_TEMP_DEBUT,
                l.DATE_TEMP_FIN,
                l.DATEANNULATION
            FROM LIEN l
            JOIN REF_LIEN rl 
                ON rl.IDREF_LIEN = l.IDREF_LIEN
            JOIN REF_TYPELIEN rt 
                ON rt.IDREF_TYPELIEN = rl.IDREF_TYPELIEN
            JOIN ENTITE_RESEAU er 
                ON er.IDINDIVIDU = l.IDINDIVIDULIE
            WHERE l.IDINDIVIDU IN {self.tuple_to_str(person_ids)}
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_entites_by_type_and_dept(self, type: str, dept: str):
        # id_pattern = f"{type}__{dept}"

        # IDENTITE must start with type
        identite_pattern = f"{type}%"
        # IDASSOCIATION must end with dept
        idasso_pattern = f"%{dept}"
        
        query = """
        SELECT IDENTITE, LIBELLEENTITE, IDASSOCIATION, IDINDIVIDU
        FROM ENTITE_RESEAU
        WHERE IDENTITE LIKE ?
        AND IDASSOCIATION LIKE ?

        """
        self.cur.execute(query, (identite_pattern, idasso_pattern))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_people_from_entite(self, entite_id: str):
        query = """
            SELECT DISTINCT
                l.IDINDIVIDU,
                l.IDREF_LIEN,
                l.DATE_TEMP_DEBUT,
                l.DATE_TEMP_FIN,
                l.DATEANNULATION,
                ia.CIVILITE,
                ia.NOM,
                ia.PRENOM,
                rl.LIBELLE_LIEN,
                rt.LIB_TYPELIEN,
                ae.ADRMAIL,
                t.INDICATIFTEL,
                t.NUMTEL,
            FROM LIEN l
            JOIN REF_LIEN rl 
                ON rl.IDREF_LIEN = l.IDREF_LIEN
            JOIN REF_TYPELIEN rt 
                    ON rt.IDREF_TYPELIEN = rl.IDREF_TYPELIEN
            JOIN INDIVIDUADRESSE ia
                ON ia.IDINDIVIDU = l.IDINDIVIDU
            JOIN ADRESSEEMAIL ae
                ON ae.IDINDIVIDU = l.IDINDIVIDU
            JOIN TELEPHONE t
                ON t.IDINDIVIDU = l.IDINDIVIDU
            WHERE l.IDINDIVIDULIE = ?;
        """
        self.cur.execute(query, (entite_id,))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_entite_info(self, entite_id: str):
        query = """
            SELECT
                er.*,
                ae.ADRMAIL,
                t.INDICATIFTEL,
                t.NUMTEL,
                ia.COMPLEMENTADR,
                ia.COMPLEMENTNUMVOIE,
                ia.CODEPOSTAL as IACODEPOSTAL,
                ia.NUMVOIE,
                ia.LIBVOIE,
                ia.LIEUDITPOSTALOUBP,
                ia.IDCIVILITE,
                ia.NOM,
                ia.PRENOM,
                ia.RAISONSOCIALE,
                ia.SIRET,
                ia.IDDEPARTEMENT,
                ia.IDTYPEINDIVIDU,

                rti.LIBTYPEINDIVIDU,
                iva.LIBVALIDITEADRESSE

            FROM ENTITE_RESEAU er
            JOIN ADRESSEEMAIL ae
                ON ae.IDINDIVIDU = er.IDINDIVIDU
            JOIN TELEPHONE t
                ON t.IDINDIVIDU = er.IDINDIVIDU
            JOIN INDIVIDUADRESSE ia
                ON ia.IDINDIVIDU = er.IDINDIVIDU
            JOIN REFTYPEINDIVIDU rti
                ON rti.IDTYPEINDIVIDU = ia.IDTYPEINDIVIDU
            JOIN REFVALIDITEADRESSE iva
                ON iva.IDVALIDITEADRESSE = ia.IDVALIDITEADRESSE

            WHERE er.IDINDIVIDU = ?;
        """
        self.cur.execute(query, (entite_id,))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_entite_info(self, entite_id: str):
        query = """
            SELECT
                er.*,
                ae.ADRMAIL,
                t.INDICATIFTEL,
                t.NUMTEL,
                ia.COMPLEMENTADR,
                ia.COMPLEMENTNUMVOIE,
                ia.CODEPOSTAL as IACODEPOSTAL,
                ia.NUMVOIE,
                ia.LIBVOIE,
                ia.LIEUDITPOSTALOUBP,
                ia.IDCIVILITE,
                ia.NOM,
                ia.PRENOM,
                ia.RAISONSOCIALE,
                ia.SIRET,
                ia.IDDEPARTEMENT,
                ia.IDTYPEINDIVIDU,

                rti.LIBTYPEINDIVIDU,
                iva.LIBVALIDITEADRESSE

            FROM ENTITE_RESEAU er
            JOIN ADRESSEEMAIL ae
                ON ae.IDINDIVIDU = er.IDINDIVIDU
            JOIN TELEPHONE t
                ON t.IDINDIVIDU = er.IDINDIVIDU
            JOIN INDIVIDUADRESSE ia
                ON ia.IDINDIVIDU = er.IDINDIVIDU
            JOIN REFTYPEINDIVIDU rti
                ON rti.IDTYPEINDIVIDU = ia.IDTYPEINDIVIDU
            JOIN REFVALIDITEADRESSE iva
                ON iva.IDVALIDITEADRESSE = ia.IDVALIDITEADRESSE

            WHERE er.IDINDIVIDU = ?;
        """
        self.cur.execute(query, (entite_id,))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_emails(self):
        self.cur.execute("SELECT DISTINCT ADRMAIL FROM ADRESSEEMAIL")
        emails = [row[0] for row in self.cur.fetchall()]
        return [" "] + emails

    def get_cd(self):
        self.cur.execute("SELECT DISTINCT ETABLISSEMENT FROM BENEVOLES_SAGE")
        cds = [row[0] for row in self.cur.fetchall()]
        return [" "] + cds

    def get_persons_by_cd(self, cd: str):
        self.cur.execute(
            "SELECT * FROM BENEVOLES_SAGE WHERE ETABLISSEMENT = ?",
            (cd,)
        )
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def close(self):
        self.cur.close()
        self.conn.close()
    
    def get_all_id_for_name(self, nom: str, prenom: str):
        if not nom or not prenom:
            return []
        query = """
            SELECT DISTINCT IDINDIVIDU
            FROM INDIVIDUADRESSE
            WHERE LOWER(NOM) = LOWER(?)
            AND LOWER(PRENOM) = LOWER(?)

            UNION

            SELECT DISTINCT IDENTIFIANTCONTACTPN
            FROM BENEVOLES_SAGE
            WHERE LOWER(NOM) = LOWER(?)
            AND LOWER(PRENOM) = LOWER(?)
        """
        print("azerty", nom, prenom)
        self.cur.execute(query, (nom, prenom, nom, prenom))
        results = self.cur.fetchall()
        return [int(row[0]) for row in results] if results else []


def convert_date(df: pd.DataFrame, col_name: str, format="%Y%m%d") -> pd.DataFrame:
    df[col_name] = pd.to_datetime(df[col_name].str[:8], format=format, errors="coerce")
    return df

def cleanup(df: pd.DataFrame, show_active: bool = False) -> pd.DataFrame:
    df["DATEANNULATION"] = df["DATEANNULATION"].replace("00000000000000000", pd.NA)

    df = convert_date(df, "DATE_TEMP_DEBUT")
    df = convert_date(df, "DATE_TEMP_FIN")
    df = convert_date(df, "DATEANNULATION", format="%Y%m%d%H%M%S%f")

    if show_active:
        today = pd.Timestamp.today()
        df = df[(df["DATEANNULATION"].isna()) | (df["DATEANNULATION"] >= today)]
        df = df[(df["DATE_TEMP_FIN"].isna()) | (df["DATE_TEMP_FIN"] >= today)]

    df = df.dropna(axis=1, how="all")
    
    return df
