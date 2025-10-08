import streamlit as st
import pandas as pd

PASSWORD = "M3jf7U9A1FjMsPVF"

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
    st.title("Bulb Install Lookup")

    @st.cache_data
    def load_csvs():
        elec_df = pd.read_csv("bulb_elec.csv")
        gas_df  = pd.read_csv("bulb_gas.csv")
        return elec_df, gas_df

    elec_df, gas_df = load_csvs()
    
    
    dataset_choice = st.radio("Select fuel to search:", ["Electricity", "Gas"])

    if dataset_choice == "Electricity":
        df = elec_df
    else:
        df = gas_df


    columns_to_show = ['Device ID', 'Meter Serial Number',  'Install Code', 'Device Model', 'Device Firmware Version']


    search_key = st.text_input(f"Enter GUID or MSN to lookup")

if search_key:
    results = df[
        (df['Device ID'].astype(str) == search_key) |
        (df['Meter Serial Number'].astype(str) == search_key)
    ]

    if not results.empty:
        results_display = results[columns_to_show]
        
        st.write(f"Found {len(results_display)} row(s):")
        st.dataframe(results_display)
        
        csv = results_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download result as CSV",
            data=csv,
            file_name=f"{dataset_choice}_lookup_{search_key}.csv",
            mime='text/csv'
        )
    else:
        st.warning("No matching records found.")
