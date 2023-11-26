import streamlit as st
import pandas as pd
import io
from sklearn.impute import SimpleImputer

# Access the uploaded dataset from the Streamlit session state
uploaded_data = st.session_state.get('uploaded_data', None)

# Check if data is uploaded
if uploaded_data is not None:
    st.title('Clean Dataset')

    st.write("""
    This page allows you to handle missing values in the dataset. You can choose to either remove specific tuples
    containing null values or fill the null values using different methods.
    """)

    # Display df.isnull().sum() with caption
    st.header('Missing Values:')
    st.write(uploaded_data.isnull().sum())
    st.caption("Number of missing values in each column.")

    # User options
    st.sidebar.subheader('Options:')
    
    # Option to fill null values
    st.sidebar.subheader('Fix Null Values:')
    fill_options = ['Select Option','Remove Tuples with Null Values', 'Mean', 'Median', 'Mode', 'Backward Fill', 'Forward Fill', 'Zero', 'Linear Interpolation', 'Custom Imputation']
    selected_method = st.sidebar.selectbox('Select Method:', fill_options)

    if selected_method == 'Remove Tuples with Null Values':
        if st.sidebar.button('Apply Method'):
            df_cleaned_rows = uploaded_data.dropna()
            df_cleaned_columns = uploaded_data.dropna(axis=1)
        
            st.success('Tuples with null values removed successfully!')
            st.write('### Cleaned Dataset (Rows):')
            st.write(df_cleaned_rows)
        
            st.write('### Cleaned Dataset (Columns):')
            st.write(df_cleaned_columns)

            # Save the cleaned dataset to a new CSV file
            df_cleaned_rows.to_csv('cleaned_dataset.csv', index=False)
            st.success('Cleaned dataset saved to cleaned_dataset.csv')

            df_filled1 = pd.read_csv('cleaned_dataset.csv')
            # Display information for cleaned_dataset.csv
            st.header('Preview of the Dataset:')
            st.write(df_filled1.head())
            st.caption("Preview of the first few rows in the dataset.")

            st.header('Dataset Shape:')
            st.write(f"The dataset has {df_filled1.shape[0]} rows and {df_filled1.shape[1]} columns.")
            st.caption("Total number of rows and columns in the dataset.")

            # Capture df_filled1.info() output
            buffer_filled = io.StringIO()
            df_filled1.info(buf=buffer_filled)
            info_output_filled = buffer_filled.getvalue()

            st.header('Dataset Information:')
            st.text(info_output_filled)
            st.caption("Summary information about the dataset, including data types and non-null values.")

            st.header('Missing Values:')
            st.write(df_filled1.isnull().sum())
            st.caption("Number of missing values in each column.")

            st.header('Summary Statistics:')
            st.write(df_filled1.describe())
            st.caption("Summary statistics for numerical columns in the dataset.")

    elif selected_method in ['Mean', 'Median', 'Mode', 'Backward Fill', 'Forward Fill', 'Zero', 'Linear Interpolation', 'Custom Imputation']:
        if st.sidebar.button('Apply Method'):
            if selected_method in ['Mean', 'Median']:
                numeric_columns = uploaded_data.select_dtypes(include=['number']).columns
                imputer = SimpleImputer(strategy=selected_method.lower())
                uploaded_data[numeric_columns] = imputer.fit_transform(uploaded_data[numeric_columns])
                df_filled = uploaded_data
            elif selected_method == 'Mode':
                df_filled = uploaded_data.fillna(uploaded_data.mode().iloc[0])
            elif selected_method == 'Backward Fill':
                df_filled = uploaded_data.fillna(method='bfill')
            elif selected_method == 'Forward Fill':
                df_filled = uploaded_data.fillna(method='ffill')
            elif selected_method == 'Zero':
                df_filled = uploaded_data.fillna(0)
            elif selected_method == 'Linear Interpolation':
                df_filled = uploaded_data.interpolate(method='linear')

            st.success(f'Null values fixed using {selected_method} successfully!')
            st.write('### Cleaned Dataset:')
            st.write(df_filled)

            # Save the filled dataset to a new CSV file
            df_filled.to_csv('cleaned_dataset.csv', index=False)
            st.success('Cleaned dataset saved to cleaned_dataset.csv')

            # Display information for cleaned_dataset.csv
            st.header('Preview of the Dataset:')
            st.write(df_filled.head())
            st.caption("Preview of the first few rows in the dataset.")

            st.header('Dataset Shape:')
            st.write(f"The dataset has {df_filled.shape[0]} rows and {df_filled.shape[1]} columns.")
            st.caption("Total number of rows and columns in the dataset.")

            # Capture df_filled.info() output
            buffer_filled = io.StringIO()
            df_filled.info(buf=buffer_filled)
            info_output_filled = buffer_filled.getvalue()

            st.header('Dataset Information:')
            st.text(info_output_filled)
            st.caption("Summary information about the dataset, including data types and non-null values.")

            st.header('Missing Values:')
            st.write(df_filled.isnull().sum())
            st.caption("Number of missing values in each column.")

            st.header('Summary Statistics:')
            st.write(df_filled.describe())
            st.caption("Summary statistics for numerical columns in the dataset.")
else:
    st.warning('Please upload a CSV file in the Upload page.')
