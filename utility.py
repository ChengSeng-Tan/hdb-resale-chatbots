import streamlit as st  
import hmac  
import pandas as pd

# """  
# This file contains the common components used in the Streamlit App.  
# This includes the data load &  the password check.  
# """  
filepath = "./data/hdb_resale_data_fr_Jan_2021.csv"

@st.cache_data
def load_data():

    df = pd.read_csv(filepath, index_col=False)
    df['month'] = pd.to_datetime(df['month'], format='%Y-%m')
    # add a new column for the price psf
    df['psf'] = df['resale_price'] / (df['floor_area_sqm']*10.7639)
    # sequence the Resale Price column towards the front
    price_col = df.pop('resale_price')
    df.insert(6, 'resale_price', price_col)
    return df

def check_password():  
    """Returns `True` if the user had the correct password."""  
    def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):  
            st.session_state["password_correct"] = True  
            del st.session_state["password"]  # Don't store the password.  
        else:  
            st.session_state["password_correct"] = False  
    # Return True if the passward is validated.  
    if st.session_state.get("password_correct", False):  
        return True  
    
    # Show input for password.  
    with st.container(border=True):
        st.write("Enter password to use chatbot")
        st.text_input(  
            "Password", type="password", on_change=password_entered, key="password"  
        )  
        
        if "password_correct" in st.session_state:  
            st.error("😕 Password incorrect")  
            return False