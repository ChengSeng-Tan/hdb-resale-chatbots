import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="About This App"
)
# endregion <--------- Streamlit App Configuration --------->

st.header(":information_source: **:blue[About this App]**")

st.write("This app leverages a range of :blue[Generative AI] tools and libraries to analyze :blue[HDB resale flat] data and website information, creating :blue[chatbots] :one::moneybag: :two::pencil: that interact with users through a user-friendly Streamlit front end. These two specialized :blue[chatbots] are designed to assist users throughout their :blue[HDB Resale Flat Buying Journey].")

st.subheader("Project Scope")
st.markdown('''
    Embarking on the journey to :blue[purchase a HDB resale flat] can feel overwhelming, but this application is here to simplify the process for you! 
    
    :one::moneybag: **:blue[Resale Price Chatbot]**: Curious about past resale prices? This chatbot lets you ask questions in natural language, helping you explore the historical prices of your preferred town areas and flat types with ease.
    
    :two::pencil: **:blue[Resale Process Chatbot]**: Have questions about eligibility, grants, documentation, timelines, or anything else related to buying a HDB resale flat? This chatbot is your go-to resource, providing clear answers and guidance every step of the way.
    
    With this app, you'll navigate the complexities of purchasing a resale flat confidently and informed!
''')

st.subheader("Objectives")
st.markdown('''
    :blue[Use cases] to streamline your search on :blue[HDB Resale Flat Prices & Process]
    
    :one::moneybag: Say goodbye to the hassle of sifting through extensive past resale listings or navigating complex charts and dashboards that may not align with your preferences. You can effortlessly filter by your preferred town areas, flat types, and sold date range, then engage in a conversation with the chatbot to obtain tailored resale price information.
    
    :two::pencil: Let our chatbot handle the heavy lifting by browsing official resale procedural information directly from the HDB website on your behalf. Simply enter your question, and sit back as it provides you with the answers you need!
''')

st.subheader("Data Sources")
st.markdown('''
    HDB Website: https://www.hdb.gov.sg/residential/buying-a-flat/buying-procedure-for-resale-flats 
    Data.gov.sg: https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view
    Resale flat prices based on registration date from Jan-2017 onwards. The App will use use the transactions from :blue[Jan-2021] as the more recent transactions are more relevant to the Resale Price Query.
''')

st.subheader("Features")
st.markdown('''
    :one::moneybag:   Filters, Past Resale Transactions, Conversational Query
            - Allow buyers to sense what they can afford (which town areas, flat types) given the history of the resale market to make a more informed decision.
    
    :two::pencil:  Pictorial Process Guide, Conversation Query
            - Provides a quick answer to your questions on the process of buying a HDB Resale Flat. 
    
    :keycap_star::house:  Home Page provides context and easy navigation with links, disclaimer, side bar with all links.
                    At the chatbot input, help text and example questions are provided.  
  
''')

st.subheader("Tools Used")

app_path = 'http://localhost:8501'
page_file_path = 'pages/Methodology.py'
page = page_file_path.split('/')[1][0:-3]  # get "page4"
st.markdown(f'''
            Go to the :point_left: <a href="{app_path}/{page}" target="_self">Methodology</a> page 
            to discover how these tools work together in the chatbots.
            ''',unsafe_allow_html=True
        )
#st.page_link("pages/4_Methodology.py", label="Discover how these tools work together in the chatbots")
st.image("./assets/tools_used.png")