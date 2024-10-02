# Imports
import streamlit as st
from helper_functions.utility import check_password
from langchain_openai import OpenAI
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool
from pathlib import Path

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
    tool_websearch = WebsiteSearchTool("https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats")

    st.markdown(":information_source::world_map:**:blue[How to Buy a HDB Resale Flat]**")

    # Print Sidebar filters and Disclaimer text
    st.sidebar.success("Select an option above :point_up_2:.")

    # Define large language model (LLM)
    llm = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    
    # Creating Agents 
    agent_planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content answering the query on {prompt}",
        backstory="""You're working on planning to reply to a query on: {prompt}.
        You collect information that helps the public who wants to buy a resale HDB flat learn about the procedures and make informed decisions.
        You have access to web search tools and other resources to gather the necessary information.""",
        tools=[tool_websearch], #<--  This is the line that includes the tool
        allow_delegation=False, # <-- This is now set to False
	    verbose=True,
        LLM=llm,
    )

    agent_writer = writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate response to answer the query: {prompt}",
        backstory="""You're working on a writing a clear, engaging reply to answer query on : {prompt}.
        You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic.
        You follow the main objectives and direction of the outline as provide by the Content Planner.""",
        allow_delegation=False, 
        verbose=True, 
        LLM=llm,
    )

# <---------------------------------- Creating Tasks ---------------------------------->
    task_plan = Task(
        description="""\
        1. Prioritize the latest information, rules and conditions to answer query: {prompt}.
        2. Identify the target audience, considering "their interests and pain points.
        3. Develop a detailed content outline, including introduction, key points, and supporting information.""",
        expected_output="""\
        A comprehensive content plan document with an outline, audience analysis, procedures, rules, and conditions.""",
        agent=agent_planner,
    )
    
    task_write = Task(
        description="""\
        1. Use the content plan to craft a reply in response to query: {prompt} based on the target audience's interests.
        2. Give an empty reponse if the query: {prompt} is not related or have low resonance to the content plan generated and abort task.
        3. Sections/Subtitles are properly named in an engaging manner.  Use bullet points where necessary.
        4. Ensure the reply is structured with an engaging introduction, insightful body, and a summarizing conclusion.
        5. Proofread for grammatical errors and alignment the common style used in property blogs.""",
        expected_output="""
        A well-written engaging reply in markdown format, ready for publication.
        Nothing else, don't comment on the result afterwards.""",
        output_file="response.md",
        agent=agent_writer,
    )

    # <---------------------------------- Creating the Crew ---------------------------------->
    crew = Crew(
        agents=[agent_planner, agent_writer],
        tasks=[task_plan, task_write], # Note that the research task is not included here
        verbose=True
    )

    # Using the "with" syntax
    with st.form(key="Prompt"):
        prompt = st.text_area("Enter your query about the process of bying a HDB Resale Flat", height=60,
                           help="e.g. What do I need to do to apply to buy a HDB Resale Flat?",
                           placeholder="What grants are available to first-time buyers of HDB Resale Flats?")
        submit_button = st.form_submit_button(label="Submit")
         
    if submit_button:
        st.toast(f"Query Submitted - {prompt}")
        st.divider() 
        
        results= crew.kickoff(inputs={'prompt': prompt})

        st.write("Answer:")
        #st.markdown({results.raw}[2:-2])

        file_path = Path("./response.md")
        with open(file_path, "r") as f:
            response_markdown = f.read()
        st.markdown(response_markdown, unsafe_allow_html=True)
        st.divider()


if __name__ == "__main__":
    main()   
