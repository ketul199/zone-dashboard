import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime
from zoneinfo import ZoneInfo
import time

# ---------------- Page Config ----------------
st.set_page_config(page_title="Zone Dashboard", layout="wide")
st.title("📊 Demand–Supply Zone Dashboard")

# ---------------- Refresh Button ----------------
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ---------------- IST Time ----------------
ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
st.caption(f"🕒 Last refreshed (IST): {ist_time.strftime('%d-%m-%Y %H:%M:%S')}")

# ---------------- GitHub RAW CSV URLs ----------------
CSV_OPTIONS = {
    "Equity Zones": "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/zones.csv",
    "75–125 Min Zones": "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/zones_25_75_125.csv",
    "15–30 Min Zones": "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/zones_15_30.csv"
}

selected_csv = st.selectbox(
    "Select zone file",
    list(CSV_OPTIONS.keys())
)

# ---------------- Force Fresh Load (NO CACHE EVER) ----------------
@st.cache_data(ttl=0)
def load_csv_from_github(raw_url):
    cache_buster = int(time.time())  # breaks GitHub + Streamlit caching
    url = f"{raw_url}?ts={cache_buster}"
    return pd.read_csv(url)

df = load_csv_from_github(CSV_OPTIONS[selected_csv])

# ---------------- Data Table ----------------
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(
    filter=True,
    sortable=True,
    resizable=True
)
gb.configure_side_bar()
gb.configure_pagination(paginationAutoPageSize=True)

AgGrid(
    df,
    gridOptions=gb.build(),
    height=650,
    fit_columns_on_grid_load=True
)
