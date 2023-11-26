import streamlit as st

def about_page():
    st.title('About DWM Mini Project')
    st.write("""
        Welcome to our Data Warehousing and Mining (DWM) Mini Project! This project is designed to guide you through a seamless process of exploring, cleaning, and visualizing your dataset.

        **1. Upload CSV Dataset:**
            - Begin by uploading your CSV dataset. This could be any dataset you want to analyze for insights.

        **2. Display Dataset Information:**
            - Explore the fundamental details of your dataset, including information about its columns and summary statistics.

        **3. Clean Dataset:**
            - Address missing values in your dataset with ease. Choose from options like dropping rows or filling null values with mean, median, or mode.

        **4. Data Visualization:**
            - Visualize your data through interactive plots such as histograms, boxplots, or scatter plots. Select the variables for the X-axis and Y-axis to uncover meaningful patterns.

        This user-friendly interface aims to make the process of data exploration and analysis intuitive and accessible. Feel free to experiment with different datasets and discover insights effortlessly!
    """)

# Include this function call in your main() function where appropriate.
about_page()
