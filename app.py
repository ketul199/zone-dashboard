import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Nifty 500 Zone Viewer", layout="wide")
st.title("📊 Nifty 500 25-75-125 min Demand–Supply Zones")

df = pd.read_csv("zones.csv")

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




