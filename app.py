import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import time
from datetime import datetime
from zoneinfo import ZoneInfo

ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))



st.set_page_config(page_title="Zone Dashboard", layout="wide")
st.title("📊 Demand–Supply Zone Dashboard")

# ---------------- Refresh Button ----------------
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

st.caption(f"🕒 Last refreshed (IST): {ist_time.strftime('%d-%m-%Y %H:%M:%S')}")

# ---------------- CSV Selection ----------------
CSV_OPTIONS = {
    "Equity Zones": "zones.csv",
    "75–125 Min Zones": "zones_25_75_125.csv",
    "15-30 Min Zones": "zones_15_30.csv"
}

selected_csv = st.selectbox(
    "Select zone file",
    list(CSV_OPTIONS.keys())
)

# ---------------- Upload Override (Session Only) ----------------
uploaded_file = st.file_uploader(
    "Upload CSV (temporary override – session only)",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.warning("⚠ Using uploaded CSV (not saved to GitHub)")
else:
    df = pd.read_csv(CSV_OPTIONS[selected_csv])

# ---------------- Data Table ----------------
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(filter=True, sortable=True, resizable=True)
gb.configure_side_bar()
gb.configure_pagination(paginationAutoPageSize=True)

AgGrid(df, gridOptions=gb.build(), height=650)
