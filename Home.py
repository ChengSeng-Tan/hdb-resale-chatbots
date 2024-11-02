# Imports
import streamlit as st
from utility import check_password

def main():
    
    # region <--------- Streamlit App Configuration --------->
    st.set_page_config(
        layout="centered",
        page_title="HDB Resale Flat Chatbots"
    )
    # endregion <--------- Streamlit App Configuration --------->
  
    st.header(":house:**:blue[HDB Resale Flat Chatbots]**")
    
    # Intro
    st.write("Buying a resale HDB flat in Singapore is challenging due to complex procedures, pricing uncertainty, and navigating grants and subsidies. Accurate pricing information is difficult to obtain, and the buying process can be overwhelming due to eligibility criteria, financing options, and documentation requirements.")
    
    # Headline for 1st Chatbot
    with st.expander("Where & What Resale Flat Type Can I Afford?",expanded=True, icon="💰"):
        col1,col2,col3 = st.columns([2,6,2])
        col1.image("./assets/wherewhat.png")
        col2.write("Filter past HDB Resale transactions according to your preferred towns and flat type. Then ask questions about the chosen resale transaction listing.")
        col3.page_link("pages/1_Where & What Can I Afford.py", label="Go to Chatbot", icon="💬")

    # Headline for 2nd Chatbot
    with st.expander("How Do I Go About Buying A Resale Flat?",expanded=True, icon="📝"):
        col4, col5, col6 = st.columns([2,6,2])
        col4.image("./assets/how.png")
        col5.write("Type in your question on HDB Resale Flat buying procedure and let the chatbot provide you clear and helpful answers.")
        col6.page_link("pages/2_How to Buy HDB Resale Flat.py", label="Go to Chatbot", icon="💬")

    # Disclaimer text
    with st.sidebar.expander("Disclaimer",expanded=True,icon="⚠️"):
        disclaimer = """
                    <strong>IMPORTANT NOTICE</strong>: This web application is a prototype developed for educational purposes only.
                    The information provided here is <strong>NOT intended for real-world usage</strong> and should not be relied 
                    upon for making any decisions, especially those related to financial, legal, or healthcare matters.
                    <strong>Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
                    You assume full responsibility for how you use any generated output.</strong>
                    
                    Always consult with qualified professionals for accurate and personalized advice.
                    """
        d = f"<p style='font-size:14px;'>{disclaimer}</p>"
        st.markdown(d, unsafe_allow_html=True)                

if __name__ == "__main__":
    main()   
