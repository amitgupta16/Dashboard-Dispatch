import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard-Dispatch",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

#-<STORE DATA FROM EXCEL IN TEMP MEMORY>------------------------------------------------
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io=r"C:\Users\AmitGupta\Desktop\Dispatch.xlsx",
        skiprows=2)
    df.columns = df.columns.str.strip()    

    ### Required columns →E, G, I, P, T, Y, AC, AD, AH, BL
    columns_to_keep = ['Invoice Date', 'Financial Customer Group', 'BP Name', 'Item Description', 
                       'Product Type Description', 'Description', 'Sales Warehouse', 'QTY',
                       'Sales Value', 'Mode of Transport 1']
    df =df[columns_to_keep]
    df["Description"] = df["Description"].astype("string").str.strip()
    return df

df = get_data_from_excel()
#--------------------------------------------</STORE DATA FROM EXCEL IN TEMP MEMORY>---


#-<MAINPAGE>------------------------------------------------------------------------

oem_sales = int(df.loc[(df["Financial Customer Group"].isin(["OEM","UNI"])) &
                   (df["Product Type Description"].isin(
                       ["Radiator","Oil Cooler","Evaporator_Serpentine","Evaporator_TAF", "Evaporator_PAF"])),
                       "Sales Value"].sum())
afmkt_sales = int(df.loc[df["Financial Customer Group"].isin(["AFM"]), "Sales Value"].sum())
job_work = int(df.loc[df["Description"].isin(["Job Work - Service"]), "Sales Value"].sum())
negative_sales = int(-df.loc[df["Sales Value"] < 0, "Sales Value"].sum())
total_sales = oem_sales + afmkt_sales + job_work - negative_sales


st.title(":bar_chart: Sales Dashboard.")
st.subheader(f"Total Sales: ₹ {total_sales:,}/-")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"OEM + Inter-Unit Sales: ₹{oem_sales:,}/-")

with col2:
    st.markdown(f"A/Mkt Sales: ₹{afmkt_sales:,}/-")

with col3:
    st.markdown(f"Job-Work Sales: ₹{job_work:,}/-")

with col4:
    st.markdown(f"Sales Return: <span style='color:red'>₹{negative_sales:,}/-</span>", unsafe_allow_html=True)


st.markdown("---")






#-EVERYTHING TO BE UPDATED BELOW (DUMMY CODE)------------------------------------------------

# #-<GRAPH ONE>----------------------------------------------------------------------
# st.write("**1. Plant-wise WIP**")
# plant_wip_df = df.groupby("Company")["Amount"].sum().sort_values()
# fig_plant_wip = px.bar(
#     plant_wip_df,
#     x= plant_wip_df.index,
#     y= "Amount",
#     labels={
#             "x": "Plants",
#             "Amount": "Amount"
#         }
# )
# st.plotly_chart(fig_plant_wip, width="stretch")
# st.markdown("---")
# #-------------------------------------------------------------------</GRAPH ONE>----


# company = sorted(df["Company"].dropna().unique())


# #-<GRAPH TWO>-----------------------------------------------------------------------

# st.write("**2. Stage-wise WIP**")
# sel_company2 = st.pills(
#     "Select the Plant/s: ",
#     options= company,
#     default= company,
#     selection_mode="multi"
# )

# if not sel_company2:
#     st.warning("Select at least one plant to view the graph.")
# else:
#     #---Make a df filtering data based on sel_company only
#     df_sel2 = df[df["Company"].isin(sel_company2)]

#     stage_wip_df = df_sel2.groupby("Stage")["Amount"].sum().sort_values(ascending=False)
#     fig_stage_wip = px.bar(
#         stage_wip_df,
#         x= stage_wip_df.index,
#         y= "Amount",
#         labels={
#             "x": "WIP-Stage",
#             "Amount": "Amount"
#         }
#     )
#     st.plotly_chart(fig_stage_wip, width="stretch")

# st.markdown("---")
# #-------------------------------------------------------------------</GRAPH TWO>----



# #-<GRAPH THREE>---------------------------------------------------------------------

# st.write("**3. Ware-House wise details**")

# sel_company3 = st.radio(
#     "Select one of the Plant: ",
#     options=company,
#     horizontal=True
# )

# #---Make a df filtering data based on sel_company only
# df_sel3 = df[df["Company"] == sel_company3]

# wh_wip_df = df_sel3.groupby("Warehouse")["Amount"].sum().sort_values(ascending=False)
# fig_wh_wip = px.bar(
#     wh_wip_df,
#     x= wh_wip_df.index,
#     y= "Amount",
#     labels={
#         "x": "Ware-House",
#         "Amount": "Amount"
#     }
# )
# st.plotly_chart(fig_wh_wip, width="stretch")
# st.markdown("---")
# #------------------------------------------------------------------</GRAPH THREE>---


#-Remove the default header, footer and main menu bar
# hide_st_style = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_st_style, unsafe_allow_html=True)
#--------------------------------------------------------------------</MAINPAGE>---