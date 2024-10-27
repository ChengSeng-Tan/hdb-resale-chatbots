import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Methodology"
)
# endregion <--------- Streamlit App Configuration --------->

st.header(":hammer_and_wrench: **:blue[Methodology]**")

st.write("Here's a peek into the :blue[internal workings] of the two :blue[chatbots] used in this Streamlit App.")

# 1st Chatbot (Ask Price)
st.subheader(":one::moneybag: Ask Resale Price Chatbox")
st.write(":man: User Interface")
st.write("""
        The user can select a :blue[date range] using a slider to define the period for viewing 
        :blue[resale transactions]. Additionally, they can choose specific :blue[towns] and :blue[flat types]. 
        Once these :blue[filters] are applied, the user can access a detailed :blue[listing of 
        transactions] and view a :blue[chart] displaying the :blue[distribution of resale prices]. 
        Furthermore, they have the option to input :blue[queries] in natural langugage 
        (no Pandas syntax needed!) related to the :blue[resale data], with :blue[answers] displayed on-screen 
        along with insights into the :blue[chatbot's processing steps].
            """
)
st.write(":robot_face: AI Chatbot Logic")
st.write("""
        A :blue[large language model (LLM)] is initialized using :blue[OpenAI's API] with a temperature 
        setting of zero to ensure precise, non-creative responses. Subsequently, a 
        :blue[Pandas DataFrame Agent:blue] is created to process user queries, enabling the return of 
        intermediate steps and actual results. Upon receiving a :blue[prompt], the agent generates 
        a response while also displaying its thought process in an expandable :blue[scratchpad] 
        section. The :blue[final output] is presented in a text area for the user to review.
            """
)
st.image("./assets/PriceChatbot_Flow.png")

# 2nd Chatbot (Ask Process)
st.subheader(":two::pencil: Ask Resale Process Chatbox")
st.write(":man: User Interface")
st.write("""
        The user can begin by viewing a :blue[pictorial process flow] that outlines the steps 
        involved in :blue[purchasing a HDB Resale Flat], providing a clear overview of the entire 
        buying process. After familiarizing themselves with these steps, they can enter 
        specific :blue[queries about the process]. Upon submission, detailed :blue[answers] are generated 
        and can be viewed :blue[on-screen].
            """
        )
st.write(":robot_face: AI Chatbot Logic")
st.write("""
        A :blue[large language model (LLM)] is initialized using :blue[OpenAI's API] with a zero temperature
        setting to ensure precise and accurate responses. The :blue[chatbot] operates through a :blue[CrewAI]
        framework, employing a sequential process that involves two primary agents: 
        a :blue[Researcher] and a :blue[Writer]. The :blue[Researcher agent] is responsible for extracting 
        detailed information about purchasing resale HDB flats, utilizing a :blue[web search tool]
        to gather data exclusively from specified websites. This agent compiles the 
        information, including relevant hyperlinks, into a comprehensive document.
        Subsequently, the :blue[Writer agent] uses the material collected by the Researcher to craft
        a clear and engaging response to the user's query, ensuring that it remains factually
        accurate and focused solely on :blue[HDB resale flats]. The final :blue[response] is then returned 
        to the user for :blue[review].
             """
             )
st.image("./assets/ProcessChatbot_Flow.png")
