import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Nifty 500 Zone Viewer", layout="wide")
st.title("📊 Nifty 500 Demand–Supply Zones")

df = pd.read_csv("EQUITY_25_75_125_MIN_demand_supply_zones_status_20260102_1712.csv")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(
    filter=True,
    sortable=True,
    resizable=True
)
gb.configure_side_bar()
gb.configure_pagination(paginationAutoPageSize=True)

gridOptions = gb.build()

AgGrid(
    df,
    gridOptions=gridOptions,
    height=650,
    fit_columns_on_grid_load=True
)




