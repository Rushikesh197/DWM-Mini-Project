import streamlit as st
import pandas as pd

def upload_csv():
    st.title('Upload CSV Data for Analysis')
    st.write("""
        This page allows you to upload a CSV file for analysis in our Data Warehousing and Mining (DWM) Mini Project.
        Please make sure your file is in CSV format.
    """)

    uploaded_file = st.file_uploader('Choose a CSV file', type=['csv'])

    if uploaded_file is not None:
        st.success('File uploaded successfully!')
        st.write('### Uploaded CSV Preview:')
        data = pd.read_csv(uploaded_file)
        st.write(data.head())

        st.write("""
            ### Next Steps:
            1. Proceed to the 'Display Dataset Information' section to explore fundamental details.
            2. Navigate to the 'Clean Dataset' section to handle missing values.
            3. Move on to the 'Data Visualization' section to create interactive plots.
        """)
        # Pass the uploaded data to the display.py script using session state
        st.session_state.uploaded_data = data

    else:
        st.warning('Please upload a valid CSV file.')

# Include this function call in your main() function where appropriate.
upload_csv()
