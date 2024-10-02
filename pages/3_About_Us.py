import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="About This App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

# st.write("This is a Streamlit App that demonstrates how to use the OpenAI API to generate text completions.")
st.write("A detailed page outlining the project scope, objectives, data sources, and features.")

with st.expander("Details about this App"):
    st.write("1. Project Scope")
    st.write("2. Objectives")
    st.write("3. Data Sources")
    st.write("4. Features")
