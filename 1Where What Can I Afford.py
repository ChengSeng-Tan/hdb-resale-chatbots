# Imports
import streamlit as st
import pandas as pd
from helper_functions.utility import check_password, load_data
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

def main():
    # Check if the password is correct.  
    if not check_password():  
        st.stop()
    
    # region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="centered",
        page_title="Query on HDB Resale Transactions"
    )
    # endregion <--------- Streamlit App Configuration --------->

    # Upload File
    #file =  st.file_uploader("Upload CSV file",type=["csv"])
    #if not file: st.stop()

    # Load the CSV file
    df = load_data()
    
    st.markdown(":heavy_dollar_sign::house:**:blue[What & Where Can I Afford?]**")

    # Print Sidebar filters and Disclaimer text
    st.sidebar.success("Select an option above :point_up_2:.")
    
    # Sidebar for Filters
    st.sidebar.header("Filters")
    selected_towns = st.sidebar.multiselect("Select Town(s)", 
                                         options=df['town'].unique(),
                                         default="ANG MO KIO",
                                         placeholder="Select town(s)")

    # Multiple selection dropdowns for flat_type 
    selected_flat_types = st.sidebar.multiselect("Select Flat Type(s)", 
                                                 options=df['flat_type'].unique(), 
                                                 default=df['flat_type'].unique(),
                                                 placeholder="Select Flat Type (default: all)")
    
    # Disclaimer text
    with st.sidebar.expander("Disclaimer"):
        st.write(f"**IMPORTANT NOTICE**: This web application is a prototype developed for educational purposes only. The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.")
        st.write("**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**")
        st.write("Always consult with qualified professionals for accurate and personalized advice.")
        st.write("")
    
    # Filter Data based on selections
    filtered_df = df[(df['town'].isin(selected_towns)) &
                 (df['flat_type'].isin(selected_flat_types))]
    
    # Dynamic title
    if not filtered_df.empty:
        listing_title = f"HDB Resale Listing of {selected_flat_types} flats in {selected_towns}"
    else:
        listing_title = "HDB Resale Listing"
    
    with st.expander(listing_title):
         st.dataframe(filtered_df, use_container_width=True)
    
    # Define large language model (LLM)
    llm = OpenAI(api_key=st.secrets['OPENAI_API_KEY'],temperature=0.0)
    
    # Define pandas df agent
    agent = create_pandas_dataframe_agent(llm, filtered_df, 
                                          verbose=True, allow_dangerous_code=True)
    
    # Using the "with" syntax
    with st.form(key="Prompt"):
        prompt = st.text_area("Enter your query about HDB Resale Prices", height=60,
                              help="e.g. What is the highest HDB flat sold. Give me a table breakdown by flat type?",
                              placeholder="What is the highest price sold for a Ang Mo Kio 4-Room flat?")
        submit_button = st.form_submit_button(label="Submit")             
        
    if submit_button:
        st.toast(f"Query Submitted - {prompt}")
        st.divider() 
        response = agent.run(prompt)
        st.write("Answer:")
        st.write(response)

if __name__ == "__main__":
    main()   

