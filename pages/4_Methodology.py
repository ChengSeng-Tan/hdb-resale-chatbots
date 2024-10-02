import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Methodology"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodoloy")

# st.write("This is a Streamlit App that demonstrates how to use the OpenAI API to generate text completions.")
st.write("A comprehensive explanation of the data flows and implementation details.")

with st.expander("Process flows for each of the use cases in the application."):
    st.write("1. A flowchart illustrating the process flow for each of the use cases in the application. For example, if the application has two main use cases: a) chat with information and b) intelligent search, each of these use cases should have its own flowchart.")
    st.write("2. Use Case a. Chat with information - Flowchart")
    st.write("3. Use Case b. Intelligent search - Flowchart")
