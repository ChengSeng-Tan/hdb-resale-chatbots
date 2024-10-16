# Imports
import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utility import check_password, load_data
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# The next 3 files are needed to resolve the sqlite3 runtime error on Streamlit Community Cloud
#__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

def main():
    
    # region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="centered",
        page_title="Query on HDB Resale Transactions"
    )
    # endregion <--------- Streamlit App Configuration --------->
 
    st.header(":moneybag: **:blue[What & Where Can I Afford?]**")   
    
    # Load the data file into session date
    if "df" not in st.session_state:
        st.session_state["df"] = load_data()
    df = st.session_state["df"] 

    # calculate the default date range for filter slider
    max_date = df["month"].max()
    min_date = df["month"].max() - relativedelta(months=12)
    # convert to datetime format
    max_date = max_date.to_pydatetime()
    min_date = min_date.to_pydatetime()
  
    # Sidebar for Filters
    st.sidebar.header(":level_slider: Filters")
    
    selected_min_date, selected_max_date = st.sidebar.slider("Select date range",
                                           df["month"].min(),
                                           df["month"].max(),
                                           (min_date, max_date),
                                           format="YYYY-MM",
                        )

    selected_towns = st.sidebar.multiselect("Select Town(s)", 
                                         options=df['town'].unique(),
                                         default=["ANG MO KIO","TOA PAYOH"],
                                         placeholder="Select town(s)")

    # Multiple selection dropdowns for flat_type 
    selected_flat_types = st.sidebar.multiselect("Select Flat Type(s)", 
                                                 options=df['flat_type'].unique(), 
                                                 default=["3 ROOM","4 ROOM"],
                                                 placeholder="Select Flat Type(s)")

    dff = df[(df['town'].isin(selected_towns)) &
                  (df['flat_type'].isin(selected_flat_types)) &
                  (df['month'] >= pd.Period(selected_min_date, freq='M').start_time) & 
                  (df['month'] <= pd.Period(selected_max_date, freq='M').end_time)
                  ]
    
    # create boxplots
    # Generate a rainbow color palette
    towns = dff["town"].unique()            # list of selected towns
    flat_types = dff["flat_type"].unique()  # list of selected flat types
    colors = ["hsl({}, 70%, 70%)".format(h) for h in np.linspace(0, 360, len(towns)*len(flat_types))]

    fig = go.Figure()
    
    # create the boxplot for each flat type within each town
    for i in range(len(towns)):
        for j in range(len(flat_types)):
          fig.add_trace(go.Box(
            y=dff[(dff['town']==towns[i]) & (dff['flat_type']==flat_types[j])]['resale_price'],
            x=dff[(dff['town']==towns[i]) & (dff['flat_type']==flat_types[j])]['town'],
            name=flat_types[j],
            marker_color=colors[j]
        ))      

    # remove duplicate legend names (flat types)
    names = set()
    fig.for_each_trace(
        lambda trace:
            trace.update(showlegend=False)
            if (trace.name in names) else names.add(trace.name))

    fig.update_layout(
    title_text="Box Plots of Resale Transacted Prices by Town and Flat Type",
    yaxis_title="Resale Price",
    xaxis_title="Town", hovermode="closest", 
    legend=dict(
        y=-0.55,
        orientation="h",
        yanchor="bottom",
        xanchor="right",
        yref="container",
        x=0.9,
    ),
    boxmode='group' # group together boxes of the different traces for each value of x  
    )
    # end of boxplot definition 
    
    # Filter line
    selected_min_date = selected_min_date.strftime("%Y-%m")
    selected_max_date = selected_max_date.strftime("%Y-%m")
    filter_line = f"Filtered on HDB Resale :red[{selected_flat_types}] flats in :red[{selected_towns}] sold from :red[{selected_min_date}] to :red[{selected_max_date}]"
    
    with st.container(border=True):
        st.write(f":level_slider: {filter_line}")
    
    tab1, tab2, tab3 = st.tabs([":speech_balloon: Ask Price", ":page_facing_up: Listing of Resale Transactions",":bar_chart: Distribution of Transacted Resale Prices by Town and Flat Type"])
             
    with tab2:
        # Format the DataFrame
        ddff = dff.style.format({
                    'resale_price': '${:,.0f}',  # Format as $
                    'floor_area_sqm': '${:.0f}',  # Format as $
                    'month': lambda x: x.strftime('%Y-%m')  # Format date
                })
        st.dataframe(ddff, use_container_width=True)
    with tab3:
        # Display overall min, max, and median resale transacted prices
        resale_price_stats = f"Transacted prices range from ${dff['resale_price'].min():,.0f} to ${dff['resale_price'].max():,.0f}; median is ${dff['resale_price'].median():,.0f}"
        #st.markdown(resale_price_stats)
        st.markdown(
            f'<p>{resale_price_stats}</p>',
            unsafe_allow_html=True
        )
        # Display boxplots by selected towns, flat types
        st.plotly_chart(fig, use_container_width=True) 

    with tab1:
        
        # Check if the password is correct.  
        if not check_password():  
            st.stop()    
       
        # Define large language model (LLM)
        llm = OpenAI(api_key=st.secrets['OPENAI_API_KEY'],temperature=0.0)
    
        # Define pandas df agent
        agent = create_pandas_dataframe_agent(llm, dff, return_intermediate_steps=True, 
                                        verbose=True, allow_dangerous_code=True)
    
        # Using the "with" syntax
        with st.form(key="Prompt"):
            prompt = st.text_area("Enter your query about HDB Resale Prices", height=45,
                                 help="e.g. What is the cheapest HDB flat sold. Give me a table breakdown by flat type?",
                                 placeholder="List the price, floor level and remaining lease of the 5 most expensive flats in Toa Payoh.\nTell me the median price. Provide a table breakdown by town, flat type, remaining lease?\nIs there a high floor 4 Room flat sold for less than $400,000?")
            submit_button = st.form_submit_button(label="Ask Price")             
        
        with st.spinner(":hourglass_flowing_sand: Searching for information.  Please wait ..."):
            if submit_button:
                st.toast(f"Query Submitted - {prompt}")
                st.divider() 

                response = agent(prompt)
                with st.expander(":gear: Chatbot's scratchpad"):
                    st.write(response["intermediate_steps"])
                st.text_area(label="",value=response["output"])
   
if __name__ == "__main__":
    main()   

