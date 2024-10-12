# Imports
import streamlit as st
from utility import check_password
from langchain_openai import OpenAI
# crewai 
from crewai import Agent, Task, Crew, Process
from crewai_tools import WebsiteSearchTool

# The next 3 files are needed to resolve the sqlite3 runtime error on Streamlit Community Cloud
#__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

def main():
    # Check if the password is correct.  
    if not check_password():  
        st.stop()
    
    # region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="centered",
        page_title="How to Buy HDB Resale Flat"
    )
    # endregion <--------- Streamlit App Configuration --------->
  
    # Create a new instance of the WebsiteSearchTool
    # Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
    website_addr = "https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats"
    tool_websearch = WebsiteSearchTool(website_addr)

    st.header(":pencil: **:blue[How to Buy a HDB Resale Flat]**")

    # Define large language model (LLM)
    llm = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    
    # Creating Agents 
    agent_researcher = Agent(
        role="Researcher",
        goal="Extract detailed information about the procedures of buying resale HDB Flats",
        backstory="""You're working on planning to reply to a query on buying HDB Resale Flats.
        You collect information from the website and links that are referenced from the pages.
        Include the full web addresses for inclusion in the final response.
        You have access to web search tools to gather the necessary information.
        Do not provide information outside the searched pages""",
        tools=[tool_websearch], #<--  This is the line that includes the tool
        allow_delegation=False, # <-- This is now set to False
	    verbose=True,
        LLM=llm,
    )

    agent_writer = Agent(
        role="Writer",
        goal="Craft an insightful and factually accurate response to answer the query: {prompt}",
        backstory="""You're working on a writing a clear, engaging reply to answer query on : {prompt}.
        You base your writing on the information gathered by the Researcher, who has compiled all information about buying on HDB Resale flats.
        You do not include other information other than buying of HDB Resale Flats.""",
        allow_delegation=False, 
        verbose=True, 
    )

# <---------------------------------- Creating Tasks ---------------------------------->
    task_research = Task(
        description="""\
        1. Only use the website to extract information.
        2. Conduct an in-depth compilation of all information on the buying of HDB Resale Flats.
        3. Include the hyperlinks of the webpages where more detailed information can be found
        4. Identify the conditions, rules and regulations, procedures in the various steps.""",
        expected_output="""\
        A comprehensive document on the requirements of buying a HDB Resale Flat in Singapore.""",
        agent=agent_researcher,
    )
    
    task_write = Task(
        description="""\
        1. Only use the Researcher's material to craft a clear, concise reply to {prompt}."
        2. Do not use any other sources.
        3. Proofread for grammatical errors
        4. Limit the reply to less than 500 words""",
        expected_output="""
        A well-written engaging reply that answers the query on the buying of HDB Resale Flat.
        Reply with a friendly error message if the query has no relevance to the buying of HDB Resale Flat.
        Nothing else, don't comment on the result afterwards.""",
        agent=agent_writer,
    )

    # <---------------------------------- Creating the Crew ---------------------------------->
    crew = Crew(
        agents=[agent_researcher, agent_writer],
        tasks=[task_research, task_write], 
        process=Process.sequential,
        verbose=True
    )

    tab1, tab2 = st.tabs([":speech_balloon: Ask Process", ":jigsaw: Overview of the HDB Resale Buying Process"])
    
    with tab1:    
        # Using the "with" syntax
        with st.form(key="Prompt"):
            prompt = st.text_area("Enter your query about the process of buying a HDB Resale Flat", height=45,
                               help="e.g. What do I need to do to apply to buy a HDB Resale Flat?",
                               placeholder="What flats can I buy, and is there a location restriction?\nWhat grants are available to first-time buyers of HDB Resale Flats?\nCan I pay for a resale flat with my CPF?")
            submit_button = st.form_submit_button(label="Ask Process")
            
        with st.spinner(":hourglass_flowing_sand: Searching for information.  Please wait ..."):
            if submit_button:
                st.toast(f"Query Submitted - {prompt}")
                st.divider() 
        
                results= crew.kickoff(inputs={'prompt': prompt})
                st.markdown(results.raw)
    with tab2:
        st.image("./assets/overview.png")

if __name__ == "__main__":
    main()   
