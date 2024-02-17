import streamlit as st
import pandas as pd
from financial_functions import load_clean, Benford, Total

def analyse():
    st.title("Financial Data Analysis")

    # File upload in sidebar
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xls", "xlsx"])
    
    if uploaded_file is not None:
        # Load and clean data
        JOURNAL = load_clean(uploaded_file)

        st.write("Data loaded and cleaned successfully!")

        # Benford's Law Analysis
        st.sidebar.subheader("Benford's Law Analysis")
        benford_fig = Benford(JOURNAL)
        st.plotly_chart(benford_fig)

        # Select time period in sidebar
        period = st.sidebar.radio("Select time period:", ('Daily', 'Weekly', 'Monthly'))

        if period == 'Daily':
            periode = 'D'
        elif period == 'Weekly':
            periode = 'W'
        else:
            periode = 'M'
        # Total Debit and Credit Analysis
        st.sidebar.subheader("Total Debit and Credit Analysis")
        total_fig = Total(JOURNAL.copy(), periode)
        st.plotly_chart(total_fig)

 

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ['Home', 'Analysis', 'About'])

    if page == 'Home':
        st.title('Home Page')
        st.write('This is the home page.')

    elif page == 'Analysis':
        st.title('Analysis Page')
        st.write('This is the analysis page.')
        analyse()

    elif page == 'About':
        st.title('About Page')
        st.write('This is the about page.')

if __name__ == "__main__":
    main()
