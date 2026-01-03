import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime
from zoneinfo import ZoneInfo
import time

st.set_page_config(page_title="Zone Dashboard", layout="wide")
st.title("📊 Demand–Supply Zone Dashboard")

# ---------------- Refresh Button ----------------
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ---------------- IST Time ----------------
ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
st.caption(f"🕒 Last refreshed (IST): {ist_time.strftime('%d-%m-%Y %H:%M:%S')}")

# ---------------- GitHub RAW URLs ----------------
CSV_OPTIONS = {
    "Equity Zones": "https://raw.githubusercontent.com/ketul199/zone-dashboard/main/zones.csv",
    "75–125 Min Zones": "https://raw.githubusercontent.com/ketul199/zone-dashboard/main/zones_25_75_125.csv",
    "15–30 Min Zones": "https://raw.githubusercontent.com/ketul199/zone-dashboard/main/zones_15_30.csv"
}

selected_csv = st.selectbox(
    "Select zone file",
    list(CSV_OPTIONS.keys())
)

# ---------------- CSV Loader (NO CACHE) ----------------
@st.cache_data(ttl=0)
def load_csv_from_github(raw_url):
    cache_buster = int(time.time())
    url = f"{raw_url}?ts={cache_buster}"
    return pd.read_csv(url)

# ---------------- Load CSV Safely ----------------
try:
    df = load_csv_from_github(CSV_OPTIONS[selected_csv])
except Exception as e:
    st.error("❌ Failed to load CSV from GitHub")
    st.code(CSV_OPTIONS[selected_csv])
    st.exception(e)
    st.stop()

# ---------------- Data Table ----------------
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(filter=True, sortable=True, resizable=True)
gb.configure_side_bar()
gb.configure_pagination(paginationAutoPageSize=True)

# AgGrid(df, gridOptions=gb.build(), height=650)




# ---------- AgGrid ----------
gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(
    filter=True,
    sortable=True,
    resizable=True
)

gb.configure_side_bar()
gb.configure_pagination(paginationAutoPageSize=True)

# 🔑 Auto-size magic
gb.configure_grid_options(
    suppressColumnVirtualisation=True,
    domLayout="normal"
)

AgGrid(
    df,
    gridOptions=gb.build(),
    height=table_height,
    fit_columns_on_grid_load=False,
    allow_unsafe_jscode=True,
)

