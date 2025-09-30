import snowflake.connector
import pandas as pd
import os

# for local testing
# import dotenv 
# laod_dotenv()

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
        self.cur.execute(
            "SELECT IDENTIFIANTCONTACTPN FROM BENEVOLES_SAGE WHERE LOWER(EMAIL1) = LOWER(?)",
            (email,)
        )
        result = self.cur.fetchone()
        return result if result else None
    
    def get_sage_info(self, person_ids: tuple[int]):
        if not person_ids:
            return None
        query = f"SELECT * FROM BENEVOLES_SAGE WHERE IDENTIFIANTCONTACTPN IN {self.tuple_to_str(person_ids)}"
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
        query = f"SELECT INDICATIFTEL, NUMTEL FROM TELEPHONE WHERE IDINDIVIDU IN {self.tuple_to_str(person_ids)}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)

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
            l.DATE_TEMP_DEBUT,
            l.DATE_TEMP_FIN,
            l.DATEANNULATION
        FROM LIEN l
        JOIN REF_LIEN rl ON rl.IDREF_LIEN = l.IDREF_LIEN
        JOIN REF_TYPELIEN rt ON rt.IDREF_TYPELIEN = rl.IDREF_TYPELIEN
        WHERE l.IDINDIVIDU IN {self.tuple_to_str(person_ids)}
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        cols = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(data, columns=cols)


    def get_emails(self):
        self.cur.execute("SELECT DISTINCT ADRMAIL FROM ADRESSEEMAIL")
        emails = [row[0] for row in self.cur.fetchall()]
        return [" "] + emails

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
