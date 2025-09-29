import os
import pandas as pd
import streamlit as st
from supabase import create_client
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Supabase_Streamlit_Modal_App")

    #Connect to Supabase
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    supabase = create_client(url, key)

    #data from Supabase
    response = supabase.table("nfl_rushing_2024_2025").select("*").execute()
    data = response.data
    df = pd.DataFrame(data)

    st.subheader("Supabase Data Table")
    st.dataframe(df)

    #graph for rushing yards by player
    if not df.empty:
        if "Name" in df.columns and "Rushing Yards" in df.columns:
            st.subheader("Rushing Yards by Player")
            fig = px.bar(df, x="Name", y="Rushing Yards", title="Rushing Yards by Player")
            st.plotly_chart(fig)
        else:
            st.warning("The required columns 'Name' and 'Rushing Yards' are not in the data.")

if __name__ == "__main__":
    main()