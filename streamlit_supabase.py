# streamlit_supabase.py
import os
import pandas as pd
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
TABLE_NAME = "nfl_rushing_2024_2025"

@st.cache_data(show_spinner=False)
def fetch_data(url: str, key: str, table: str) -> pd.DataFrame:
    if not url or not key:
        return pd.DataFrame()
    client = create_client(url, key)
    resp = client.table(table).select("*").execute()
    data = resp.data or []
    return pd.DataFrame(data)

def main():
    st.set_page_config(page_title="2024–2025 NFL Rushing Stats", layout="wide")
    st.title("2024–2025 NFL Rushing Stats")

    if not SUPABASE_URL or not SUPABASE_KEY:
        st.warning("Missing SUPABASE_URL / SUPABASE_KEY")
        st.stop()

    df = fetch_data(SUPABASE_URL, SUPABASE_KEY, TABLE_NAME)

    if df.empty:
        st.warning("No data returned. Check credentials and table name.")
        st.stop()

    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()