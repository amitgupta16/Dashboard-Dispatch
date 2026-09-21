import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard-Dispatch",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

#-<STORE DATA FROM EXCEL IN TEMP MEMORY>------------------------------------------------
@st.cache_data
def get_data_from_excel():
    # df = pd.read_excel(io=r"C:\Users\AmitGupta\Desktop\Dispatch.xlsx", skiprows=2)
    df = pd.read_excel(io=r"C:\Users\amit.gupta\OneDrive - Pranav Vikas India Pvt. Ltd\Desktop\Dispatch.xlsx", skiprows=2)
    
    df.columns = df.columns.str.strip()
    df["Description"] = df["Description"].str.strip()
    df["BP Name"] = df["BP Name"].str.strip()

    df.rename(columns={"QTY": "Quantity"}, inplace=True)

    ### Required columns →E, G, I, P, T, Y, AC, AD, AH, BL
    columns_to_keep = ['Invoice Date', 'Financial Customer Group', 'BP Name', 'Item Description',
                    'Product Type Description', 'Description', 'Sales Warehouse', 'Quantity',
                    'Sales Value', 'Mode of Transport 1']
    df = df[columns_to_keep]

    products = ["Radiator","Oil Cooler","Evaporator_Serpentine","Evaporator_TAF","Evaporator_PAF"]
    df = df[(df["Product Type Description"].isin(products)) &
            (df["Sales Warehouse"]=="WHR100")]

    df["Product"] = df["Product Type Description"].replace({
        "Evaporator_Serpentine": "Evaporator",
        "Evaporator_TAF": "Evaporator",
        "Evaporator_PAF": "Evaporator"
        })

    df["Mode of Transport"] = np.where(df["Mode of Transport 1"]== "REEYA SAFELOGISTICS ", "Air", "Road")
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


col1, col2 = st.columns(2)

#-<GRAPH ONE>-----------------------------------------------------------------------
with col1:
    st.markdown("**1. Product-wise Sales**")
    sel_unit_1 = st.radio("Select Unit: ", 
                        options=["Quantity","Sales Value"], 
                        horizontal=True, 
                        key="sel_unit_1")


    graph_table_1 = df.groupby("Product Type Description")[sel_unit_1].sum().sort_index(ascending=False)
    graph_1 = px.bar(
        graph_table_1,
        x= graph_table_1.index,
        y= sel_unit_1,
        labels={
            "x": "Product",
            "y": sel_unit_1
        }
    )
    st.plotly_chart(graph_1, width="stretch")

#-------------------------------------------------------------------</GRAPH ONE>----




  

#-<GRAPH TWO>-----------------------------------------------------------------------
with col2:
    st.markdown("**2. Segment-wise Sales**")
    sel_unit_2 = st.radio("Select Unit: ", 
                        options=["Quantity","Sales Value"], 
                        horizontal=True, 
                        key="sel_unit_2")

    graph_table_2 = df.groupby("Financial Customer Group")[sel_unit_2].sum().sort_index(ascending=False)
    graph_2 = px.bar(
        graph_table_2,
        x= graph_table_2.index,
        y= sel_unit_2,
        labels={
            "x": "Segment",
            "y": sel_unit_2
        }
    )
    st.plotly_chart(graph_2, width="stretch")

#-------------------------------------------------------------------</GRAPH TWO>----  
    
st.markdown("---")






#-<GRAPH THREE>----------------------------------------------------------------------

st.markdown("**3. Daily Sales**")
sel_unit_3 = st.radio("Select Unit: ", 
                      options=["Quantity","Sales Value"], 
                      horizontal=True, 
                      key="sel_unit_3")

graph_table_3 = df.groupby(["Invoice Date","Product"])[sel_unit_3].sum().reset_index().sort_values("Invoice Date")
graph_3 = px.line(
    graph_table_3,
    x="Invoice Date",
    y=sel_unit_3,
    color="Product",
    markers=True
)

graph_3.update_traces(
    line=dict(color="green"),
    selector=dict(name="Oil Cooler")
)
# to make every date visible in %d-%b format → 01-Jan
graph_3.update_xaxes(
    dtick="D1",
    tickformat="%d-%b",
    # tickangle=0
)

graph_3.update_layout(
    xaxis_title="Date",
    yaxis_title=sel_unit_3,
    legend_title="Product Type",
    # hovermode="x unified"
)

st.plotly_chart(graph_3, width="stretch")
st.markdown("---")

#-----------------------------------------------------------------</GRAPH THREE>----








#-<GRAPH FOUR>----------------------------------------------------------------------

st.markdown("**4. Product Sales**")

sel_seg_4 = st.radio("Select Sales Segment: ", 
                      options=["OEM","UNI", "AFM"], 
                      horizontal=True, 
                      key="sel_seg_4")

if sel_seg_4 == "AFM":
    dd4_model = sorted(df.loc[df["Financial Customer Group"] == "AFM","Item Description"].unique())

else:
    dd4_customer = sorted(df.loc[df["Financial Customer Group"] == sel_seg_4,"BP Name"].unique())
    sel_cust_4 = st.selectbox("Select a customer from the list:",
                            options=dd4_customer,
                            key="sel_cust_4")

    dd4_model = sorted(df.loc[df["BP Name"] == sel_cust_4,"Item Description"].unique())

sel_model_4 = st.selectbox("Select a model from the list:",
                          options=dd4_model,
                          key="sel_model_4")


df_4 = df[df["Item Description"] == sel_model_4]

graph_table_4 = df_4.groupby(["Invoice Date","Mode of Transport"])["Quantity"].sum().reset_index()

pivot_4 = graph_table_4.pivot(
        index='Invoice Date', 
        columns='Mode of Transport', 
        values='Quantity').fillna(0)

graph_4 = px.bar(
    pivot_4,
    labels={
        "value": "Quantity",
        "Invoice Date": "Date"
            },
    color_discrete_map={
        "Air": "#E74C3C",
        "Road": "#0B70C7"
    }
)

graph_4.update_xaxes(
    dtick="D1",
    tickformat="%d-%b",
)

st.plotly_chart(graph_4, width="stretch")
st.markdown("---")

#-----------------------------------------------------------------</GRAPH FOUR>----












#-EVERYTHING TO BE UPDATED BELOW (DUMMY CODE)------------------------------------------------



# product_1 = ["Radiator","Oil Cooler","Evaporator"]
# sel_product = st.pills(
#     "Select the Product/s: ",
#     options= product_1,
#     default= product_1,
#     selection_mode="multi"
# )



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