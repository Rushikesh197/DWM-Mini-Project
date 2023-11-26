import streamlit as st
import pandas as pd
import io

def display_dataset_details(data):
    st.title('Dataset Overview and Analysis')

    # Display df.head() with caption
    st.header('Preview of the Dataset:')
    st.write(data.head())
    st.caption("Preview of the first few rows in the dataset.")

    # Display df.shape with caption
    st.header('Dataset Shape:')
    st.write(f"The dataset has {data.shape[0]} rows and {data.shape[1]} columns.")
    st.caption("Total number of rows and columns in the dataset.")

    # Capture df.info() output
    buffer = io.StringIO()
    data.info(buf=buffer)
    info_output = buffer.getvalue()

    # Display df.info() with caption
    st.header('Dataset Information:')
    st.text(info_output)
    st.caption("Summary information about the dataset, including data types and non-null values.")
    
    # Display df.isnull().sum() with caption
    st.header('Missing Values:')
    st.write(data.isnull().sum())
    st.caption("Number of missing values in each column.")

    # Display df.describe() with caption
    st.header('Summary Statistics:')
    st.write(data.describe())
    st.caption("Summary statistics for numerical columns in the dataset.")

def main():
    st.set_page_config(
        page_title="DWM Mini Project",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title('Displaying Preliminary Information About The Uploaded dataset')

    # Check if there is uploaded data in session state
    if hasattr(st.session_state, 'uploaded_data'):
        data = st.session_state.uploaded_data
        # Display details for the uploaded CSV data
        display_dataset_details(data)

if __name__ == '__main__':
    main()
