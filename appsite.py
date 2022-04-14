# Importing Libraries
import datetime
from io import StringIO
from re import M, X
from time import time
# from turtle import width
import pandas as pd
import streamlit as st
# import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
import plotly.figure_factory as ff
# from PIL import Image

#Temp Data assigning
df = pd.read_csv("./Affirm__Report.csv")

# # Uploading and reading a CSV File less than 200 MB - in sidebar
# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#      # Can be used wherever a "file-like" object is accepted:
#      dataframe = pd.read_csv(uploaded_file)
#      st.success('Datasheet loaded!')
#      df =dataframe


df = df.copy()
df['Description']= df['Incident Nature']+df['Incident Type']
df['Incident No.'] = df.index

# Sidebar Content
st.sidebar.title("Options")

# Providing Main site filtering option - in sidebar
site_selectbox = st.sidebar.selectbox(
    "Which Site ?",
    ('MTF', 'SEZ', 'Off Site', 'C2', 'DTA', 'KYA 6,7,8', 'PCG',
       'Common','JMD')
)

zone_selectbox_values=df[df['Unit']==site_selectbox]['Zone'].unique()

all_val=['All']
zone_selectbox_values = np.append(all_val,zone_selectbox_values)
# st.write(zone_selectbox_values)

zone_selectbox = st.sidebar.selectbox(
    f"and ... Zone from - {site_selectbox} !",
    (zone_selectbox_values)
)
#-----All to be added in Zone

function_selectbox = st.sidebar.selectbox(
    "are we looking for Function, also ?",
    ('All','Physical Security', 'Traffic', 'Automation')
)

keyword_acceptor =""
# keyword_acceptor = st.sidebar.text_input('Insert a EC|EP or Keyword')

# Data correction before displaying
# DeepCopy
df = df.copy()

# overwriting data after changing format
df["Incident Date"]= pd.to_datetime(df["Incident Date"])
df["Reporting Date"]= pd.to_datetime(df["Reporting Date"])

# Adding new columns for better and faster analysis
df['year']  = pd.DatetimeIndex(df['Incident Date']).year
df['month'] = pd.DatetimeIndex(df['Incident Date']).month
df['date']  = pd.DatetimeIndex(df['Incident Date']).day
df['weekday']  = pd.DatetimeIndex(df['Incident Date']).weekday

# Creating new data frame : Site wise
if site_selectbox =="JMD":
    df_temp = df
else:
    df_temp = df[df['Unit']==site_selectbox]

if function_selectbox !="All":
    df_temp = df_temp[df_temp['Function']==function_selectbox]

if zone_selectbox !="All":
    df_temp = df_temp[df_temp['Zone']==zone_selectbox]

if keyword_acceptor !="":
    df_temp = df_temp.loc[df_temp['Description'].str.contains(keyword_acceptor, case=False)]

# Functions
@st.cache
def convert_df(df_temp):
    return df.to_csv().encode('utf-8')

# Selected option : Site wise Configuration
st.title(f"{site_selectbox} : AFFIRM Incidents [{function_selectbox}]")
st.write("To analyse incident reports of all available years and find out the correlation between present data and identify incidents increasing trend or decreasing downfall and then suggest possible measures and focusing area's for improvement;")


# Displaying main counts from site data
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row2_1:
    columns = len(df_temp.columns)
    st.markdown("📋 " + str(columns) + " Columns")

with row2_2:
    rows = len(df_temp)
    st.markdown("🚥 " + str(rows) + " Rows")

with row2_3:
    unique_Function_Count = df_temp['Incident Nature'].nunique()
    st.markdown("🔥 " + str(unique_Function_Count) + " Inci-Nature")

with row2_4:
    unique_Function_Count = df_temp['Incident Type'].nunique()
    st.markdown("📊 " + str(unique_Function_Count) + " Inci-Type")


# Displaying raw Site dataframe with expander field
row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
with row3_1:
    st.markdown("")
    see_data = st.expander('You can click here to see the raw data first 👉')
    with see_data:
        st.dataframe(data=df_temp.reset_index(drop=True))
        # # Displaying dataframe of site
        # st.write(df[df['Unit']==site_selectbox])
        csv = convert_df(df_temp)
        st.download_button(
        label="Press to Download",
        data = csv,
        file_name=str(site_selectbox) + "_AFFIRM_Incidents.csv",
        mime="text/csv",
        key='download-csv'
        )
st.text('')

# Displaying bar char of selected site 
st.write(f"Incidents occured and recorded in various years of {site_selectbox} Site, at {zone_selectbox} Zones for {function_selectbox} functions")
st.write(f"")
st.bar_chart(df_temp["year"].value_counts().sort_index())

# Description of chart data
st.info(f"In '{site_selectbox}' : "+ str(int(df_temp["year"].value_counts().idxmax())) +", was the most hactic years in terms of incidents occurances, a highest of "+str({df_temp["year"].value_counts().max()})+" incidents reported during that year, wereas "+str(int(df_temp["year"].value_counts().idxmin()))+" remained as supper calm year in which a total of "+str({df_temp["year"].value_counts().min()})+" incidents were recorded")

st.write(" ")
st.write(" ")



## TimeFrame by Incident
st.write(f"**Timeframe by incidents of {site_selectbox} site**")

st.write(f"This section talks about dangerous Timeframes for '{site_selectbox}' site & other selected fields- tells us which Month, Date or Day has more number of incidents then others;")
st.write(" The data can further be improved and can provide wonderful insights like is it Daytime or nighttime which causes more incidents ? and help us in taking proactive solutions to tackle upcoming challenges ")
st.write(" ")

# Further filtering Site selected data 
col1, col2, col3 = st.columns(3)

with col1:
    Site_TF_selectbox = st.selectbox(
    "Select Timeframe",
    ["Month","Date","Day"])
    
with col2:
    date_from = st.date_input("From",value=df_temp['Incident Date'].min(),min_value=df_temp['Incident Date'].min(),max_value=datetime.date.today()
    )
    date_from= pd.to_datetime(date_from)
    
with col3:    
    date_till = st.date_input("Till",value=df_temp['Incident Date'].max(),min_value=date_from,max_value=datetime.date.today()
    )
    date_till= pd.to_datetime(date_till)

# Date Filter as per given dates
df_temp_date = df_temp[df_temp['Incident Date'] >=date_from]
df_temp_date = df_temp_date[df_temp_date['Incident Date'] <=date_till]

if Site_TF_selectbox=="Month":
    Site_TF_selectbox_value = "month"
elif Site_TF_selectbox=="Date":
    Site_TF_selectbox_value = "date"
elif Site_TF_selectbox=="Day":
    Site_TF_selectbox_value = "weekday"
    st.write("0 - Monday | 6- Sunday")
else:
    Site_TF_selectbox_value = ""

# Displaying main counts from site timeframe incident data
row3_spacer1, row3_1, row3_spacer2, row3_2, row3_spacer3, row3_3, row3_spacer4, row3_4, row3_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row3_1:
    columns = len(df_temp_date.columns)
    st.markdown("📋 " + str(columns) + " Columns")

with row3_2:
    rows = len(df_temp_date)
    st.markdown("🚥 " + str(rows) + " Rows")
    #-----Date formatting required correction while inserting data

with row3_3:
    unique_Function_Count = df_temp_date[Site_TF_selectbox_value].nunique()
    st.markdown("🔥 " + str(unique_Function_Count) + " Inci-Nature")

with row3_4:
    unique_Function_Count = df_temp_date['Incident Type'].nunique()
    st.markdown("📊 " + str(unique_Function_Count) + " Inci-Type")

# Displaying raw Site dataframe with expander field
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.markdown("")
    see_data = st.expander('You can click here to see the raw data first 👉')
    with see_data:
        st.dataframe(data=df_temp_date.reset_index(drop=True))
        # # Displaying dataframe of site
        # st.write(df[df['Unit']==site_selectbox])
        csv = convert_df(df_temp_date)
        st.download_button(
        label="Press to Download",
        data = csv,
        file_name=str(site_selectbox) + "_AFFIRM_Incidents.csv",
        mime="text/csv",
        key=str(site_selectbox) +'download-csv'
        )
st.text('')

#Bar Chart
st.bar_chart(df_temp_date[Site_TF_selectbox_value].value_counts().sort_index())

# Description of chart data
st.info(f"In '{site_selectbox}' : for given Timestamp i.e -"+ str(date_from) +" till "+str(date_till)+" -- " +str(Site_TF_selectbox)+" wise analysis says, {"+
str(int(df_temp_date[Site_TF_selectbox_value].value_counts().idxmax()))+"} "+str(Site_TF_selectbox)+" has encountered heighest number of incidents that is "+str(int(df_temp_date[Site_TF_selectbox_value].value_counts().max()))+"; and the minimum number of incidents was recorded on "+str(int(df_temp_date[Site_TF_selectbox_value].value_counts().idxmin()))+" "+str(Site_TF_selectbox)+" {"+str(int(df_temp_date[Site_TF_selectbox_value].value_counts().min()))+"}")



# Further filtering Site selected data 
col4, col5 = st.columns([0.60, 0.40])
with col4:

    dict_status ={}
    dict_status = df_temp_date['Status'].value_counts()

    #Data status for selected fields
    fig = px.pie(df_temp_date, values=dict_status.values, names=dict_status.keys(), color_discrete_sequence=px.colors.sequential.Bluyl,width=500,height=500)
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
    
with col5:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" **Data Frame Status** ")
    st.write(" ")
    st.write(f"This chart shows the status of '{site_selectbox}' site for '{zone_selectbox}' zones and '{function_selectbox}' Functions held in between '{date_from}' and '{date_till}'")
    st.write("*The status of incidents tells how many incidents were approved and how many are under consideration or not approved*")
    st.write(f"{df_temp_date['Status'].value_counts()}")


# Further filtering Site selected data 
col6, col7 = st.columns([0.40, 0.60])
with col6:
    st.write(" ")
    st.write(" **Incident Categories** ")
    st.write(" ")
    st.write(f"This chart shows the status of '{site_selectbox}' site for '{zone_selectbox}' zones and '{function_selectbox}' Functions held in between '{date_from}' and '{date_till}'")
    st.write("*The categories of incidents is nothing but major head in which all these incidents falls and which helps in better analysis*")
    st.write(f"{df_temp_date['Category'].value_counts()}")
    
with col7:
    dict_category ={}
    dict_category = df_temp_date['Category'].value_counts()

    #Categories of selected fields
    fig = px.pie(df_temp_date, values=dict_category.values, names=dict_category.keys(), color_discrete_sequence=px.colors.sequential.RdBu,width=500,height=500)
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
    # fig.show()


## Search anything

# url = "https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py"
# st.write("[Search a EC|EP Involvement !](%s)" % url)

# st.write(f"**Search anything from {site_selectbox} site**")
# st.write(f"This section helps you find any individual involvement by keywords in any given cases out of the sidebar selected fields. It also helps in analysing entered keyword and it's occurances")
# st.write("FS,BS,FB,MT")


# entered_ecp = st.text_input('Insert a EC|EP or - Keyword')
# st.write('The entered Keyword is :', entered_ecp)

# if(entered_ecp[0:3]=="///"):
#     if(entered_ecp[3:5]=="FS"):
#         entered_ecp = str(" ")+entered_ecp[5:]
#         st.write(f"fsYes, {entered_ecp}")
#     elif(entered_ecp[3:5]=="BS"):
#         entered_ecp = entered_ecp[5:]+str(" ")
#         st.write(f"bsYes, {entered_ecp}")
#     elif(entered_ecp[3:5]=="FB"):
#         entered_ecp = str(" ")+entered_ecp[5:]+str(" ")
#         st.write(f"fbYes, {entered_ecp}")
#     elif(entered_ecp[3:5]=="MT"):
#         st.write("mtYes")
#     else:
#         st.write("only///")
# else:
#     st.write("No")


# number = st.number_input('Insert a EC|EP number', min_value=11111111, max_value=999999999)
# st.write('The entered EC|EP number is ', number)

# col1, col2 = st.columns([0.30, 0.70])

# with col1:
#     entered_ecp = st.text_input('Insert a EC|EP or -- Keyword',help="for special search type: /// and then FS - for Including forward space")
    
# with col2:
#     if(entered_ecp[0:3]=="///"):
#         if(entered_ecp[3:5]=="FS"):
#             entered_ecp = str(" ")+entered_ecp[5:]
#             # st.write(f"fsYes, {entered_ecp}")
#         elif(entered_ecp[3:5]=="BS"):
#             entered_ecp = entered_ecp[5:]+str(" ")
#             # st.write(f"bsYes, {entered_ecp}")
#         elif(entered_ecp[3:5]=="FB"):
#             entered_ecp = str(' ')+entered_ecp[5:]+str(' ')
#             # st.write(f"fbYes, {entered_ecp}")
#         elif(entered_ecp[3:5]=="MT"):
#             st.write("") #mtYes
#         else:
#             st.write("") #only///
#     else:
#         st.write("") #NO
#     df_temp_ecp=df_temp.loc[df_temp['Description'].str.contains(entered_ecp, case=False)]
#     st.markdown("")
#     # st.text('')
#     see_data = st.expander('You can click here to see the raw data first 👉')
#     with see_data:
#         st.dataframe(data=df_temp_ecp.reset_index(drop=True))
#         # # Displaying dataframe of site
#         # st.write(df[df['Unit']==site_selectbox])
#         csv = convert_df(df_temp_ecp)
#         st.download_button(
#         label="Press to Download",
#         data = csv,
#         file_name=str(site_selectbox) + "_AFFIRM_Incidents.csv",
#         mime="text/csv",
#         key='download_report_of_'+str(entered_ecp)+'_csv'
#         )

# st.write('The entered Keyword is :', entered_ecp)
# st.button(f"Total Occurances:{len(df_temp_ecp)}",disabled=True)

# #Bar Chart
# st.bar_chart(df_temp_ecp['Unit'].value_counts().sort_index())

# st.write(" ")



st.write("--------------------------------------------------------------------------------------------------------")

st.write("**The sole purpose for building this webapp's was to analysye all site's incident data in faster and effective way!**" +
" During my analysis phase it has been found out that the analysis can be done more strongly on many aspects few of which are listed below: ")
st.write("1. What is the origin of gulty individuals and what type of crime they do - *By doing this we can take proactive measure and assist HR to be more vigilant when hiring individuals of similar traits*")
st.write("2. On which time specific incidents happens? is there any corelation with Weather, Events, Shutdowns..! - *This will help us to know in advance which type of incidents are about to come and will not only help in prepare in advance but also help in mitegate the incidents*")
st.write("3. Live data comparision -*Will proved us faster analytics and help us in driving insights faster*")

st.write(" ")
st.write(" ")
st.write("**Error | Upgradation Margin:**")
st.write("1. DateTime stamp formatting - In progress")
st.write("2. Incident Nature and Type wise analysis and outcomes")
st.write("3. Custom Affirm data upload + validation -> Insights")
st.write("4. Authentication activation")
st.write("5. Cloud storage integration")

# # Displaying raw Site dataframe with expander field
# row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
# with row4_1:
#     st.markdown("")
#     see_data = st.expander("**Error | Upgradation Margin:** 👉")
#     with see_data:
#         st.write("1. DateTime stamp formatting")
#         st.write("2. Incident Nature and Type wise analysis and outcomes")
#         st.write("3. Custom Affirm data upload + validation -> Insights")
#         st.write("4. Authentication activation")
#         st.write("5. Cloud storage integration")
        



# # Testing
# dict_incident_nature ={}
# dict_incident_nature = df_temp_date['Incident Nature'].value_counts()

# st.bar_chart(df_temp_date['Incident Nature'].value_counts())




# # Incident Nature wise Analysis
# chart_data = pd.DataFrame(
#     df_temp_date,
#     # np.random.rand(39, 4),
#     index=df_temp_date['Incident Nature'].value_counts().index,
# )

# data = pd.melt(chart_data.reset_index(), id_vars=["index"])

# # Horizontal stacked bar chart
# chart = (
#     alt.Chart(data)
#     .mark_bar()
#     .encode(
#         x=alt.X("value", type="quantitative", title=""),
#         y=alt.Y("index", type="nominal", title=""),
#         color=alt.Color("variable", type="nominal", title=""),
#         order=alt.Order("variable", sort="descending"),
#     )
# )
# st.altair_chart(chart, use_container_width=True)
