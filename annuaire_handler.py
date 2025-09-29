import snowflake.connector
import pandas as pd
import os

class AnnuaireHandler:
    def __init__(self):
        self.conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
        )
        self.cur = self.conn.cursor()

    def get_emails(self):
        self.cur.execute("SELECT DISTINCT ADRMAIL FROM ADRESSEEMAIL")
        emails = [row[0] for row in self.cur.fetchall()]
        return [" "] + emails

    def get_person_functions(self, email: str):
        query = """
        SELECT 
            rl.LIBELLE_LIEN,
            rt.LIB_TYPELIEN,
            l.DATE_TEMP_DEBUT,
            l.DATE_TEMP_FIN,
            l.DATEANNULATION
        FROM ADRESSEEMAIL am
        JOIN LIEN l ON l.IDINDIVIDU = am.IDINDIVIDU
        JOIN REF_LIEN rl ON rl.IDREF_LIEN = l.IDREF_LIEN
        JOIN REF_TYPELIEN rt ON rt.IDREF_TYPELIEN = rl.IDREF_TYPELIEN
        WHERE LOWER(am.ADRMAIL) = LOWER(:1)
        """
        self.cur.execute(query, (email,))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_person_address(self, email: str) -> pd.DataFrame:
        query = """
        SELECT 
            ia.CIVILITE,
            ia.IDCIVILITE,
            ia.ACHEMINEMENT,
            ia.CODEPOSTAL,
            ia.COMPLEMENTADR,
            ia.COMPLEMENTNOM,
            ia.LIBVOIE,
            ia.LIEUDITPOSTALOUBP,
            ia.NOM,
            ia.NUMVOIE,
            ia.PRENOM,
            ia.CODEACTIONRECRUT,
            ia.IDINDIVIDU
        FROM ADRESSEEMAIL am
        JOIN INDIVIDUADRESSE ia 
            ON ia.IDINDIVIDU = am.IDINDIVIDU
        WHERE LOWER(am.ADRMAIL) = LOWER(:1);
        """
        self.cur.execute(query, (email,))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

    def get_person_phones(self, email: str) -> pd.DataFrame:
        query = """
        SELECT 
            t.IDINDIVIDU,
            t.INDICATIFTEL,
            t.NUMTEL
        FROM ADRESSEEMAIL am
        JOIN TELEPHONE t 
            ON t.IDINDIVIDU = am.IDINDIVIDU
        WHERE LOWER(am.ADRMAIL) = LOWER(:1);
        """
        self.cur.execute(query, (email,))
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)


    def get_person_functions_name(self, nom: str, prenom: str):
        query = """
        SELECT 
            ia.IDINDIVIDU,
            rl.LIBELLE_LIEN,
            rt.LIB_TYPELIEN,
            l.DATE_TEMP_DEBUT,
            l.DATE_TEMP_FIN,
            l.DATEANNULATION
        FROM INDIVIDUADRESSE ia
        JOIN LIEN l ON l.IDINDIVIDU = ia.IDINDIVIDU
        JOIN REF_LIEN rl ON rl.IDREF_LIEN = l.IDREF_LIEN
        JOIN REF_TYPELIEN rt ON rt.IDREF_TYPELIEN = rl.IDREF_TYPELIEN
        WHERE LOWER(ia.NOM) = LOWER(:1)
          AND LOWER(ia.PRENOM) = LOWER(:2)
        ORDER BY rl.LIBELLE_LIEN, l.DATE_TEMP_DEBUT;
"""

    def close(self):
        self.cur.close()
        self.conn.close()


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
