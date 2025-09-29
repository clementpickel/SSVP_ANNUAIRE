# SSVP_ANNUAIRE

This project is a **Streamlit app** that connects to Snowflake and displays data from the SSVP annuaire.  

---

## 1. Setup Python Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment (PowerShell example):

```powershell
./.venv/Scripts/Activate.ps1
```

> For Linux/Mac, use:
>
> ```bash
> source .venv/bin/activate
> ```

---

## 2. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Fill `.env` with your Snowflake credentials:

```env
SNOWFLAKE_USER=""
SNOWFLAKE_PASSWORD=""
SNOWFLAKE_ACCOUNT=""
SNOWFLAKE_WAREHOUSE=""
SNOWFLAKE_DATABASE=""
SNOWFLAKE_SCHEMA=""
```

> Make sure to **never commit your `.env` file** to version control.

---

## 4. Run the Streamlit App

Start the app with:

```bash
streamlit run streamlit_app.py
```

* The app will open in your default browser, usually at: `http://localhost:8501`
* Streamlit automatically reloads when you save changes to your code.

---

## 5. Notes

* Ensure your Snowflake credentials have access to the specified database and schema.
* For production deployment, consider using `st.cache_resource` for the Snowflake connector to avoid opening multiple connections.

