import streamlit as st
import pandas as pd

PASSWORD = st.secrets["PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    password_input = st.text_input("Enter password:", type="password")
    login_button = st.button("Login")
    
    if login_button:
        if password_input == PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("Incorrect password")

if st.session_state.logged_in:
    st.title("Bulb Installs Lookup App")

    @st.cache_data
    def load_csvs():
        elec_df = pd.read_csv("bulb_elec.csv")
        gas_df  = pd.read_csv("bulb_gas.csv")
        return elec_df, gas_df

    elec_df, gas_df = load_csvs()
    
    dataset_choice = st.radio("Select fuel to search:", ["Electricity", "Gas"])
    df = elec_df if dataset_choice == "Electricity" else gas_df

    columns_to_show = ['Device ID', 'Meter Serial Number', 'Install Code', 'Device Model', 'Device Firmware Version']

    search_key = st.text_input(f"Enter Device ID or Meter Serial Number to lookup")
    results = pd.DataFrame()  # initialize to avoid NameError

    if search_key:
        results = df[
            (df['Device ID'].astype(str) == search_key) |
            (df['Meter Serial Number'].astype(str) == search_key)
        ]
    
    if not results.empty:
        results_display = results[columns_to_show]
        
        st.write(f"Found {len(results)} row(s):")
        st.dataframe(results_display)
        
        csv = results_display.to_csv(index=False).encode('utf-8')
    else:
        if search_key:
            st.warning("No matching records found.")

