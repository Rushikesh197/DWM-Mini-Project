import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px
import base64 

def classification_page():
    st.title('Classification Page')

    # Load the cleaned dataset from the "Clean Dataset" page
    cleaned_data = pd.read_csv('cleaned_dataset.csv')  # Update the file path if needed

    st.write("""
        This page allows you to apply classification methods such as Naive Bayes, K-Means, and Apriori.
    """)

    # Naive Bayes Classification
    st.header('Naive Bayes Classification')
    st.write("""
        Please select the target column (the column you want to predict) and the features for training the model.
    """)
    target_column_nb = st.selectbox('Select Target Column:', cleaned_data.columns)
    feature_columns_nb = st.multiselect('Select Feature Columns:', cleaned_data.columns)

    if st.button('Apply Naive Bayes'):
        if target_column_nb and feature_columns_nb:
            X_nb = cleaned_data[feature_columns_nb]
            y_nb = cleaned_data[target_column_nb]

            # Split the data into training and testing sets
            X_train_nb, X_test_nb, y_train_nb, y_test_nb = train_test_split(X_nb, y_nb, test_size=0.2, random_state=42)

            # Create and train the Naive Bayes model
            model_nb = GaussianNB()
            model_nb.fit(X_train_nb, y_train_nb)

            # Evaluate the model
            accuracy_nb = model_nb.score(X_test_nb, y_test_nb)
            st.success(f'Naive Bayes Model Accuracy: {accuracy_nb:.2f}')

            # Visualize Naive Bayes results
            y_pred_nb = model_nb.predict(X_test_nb)
            results_nb = pd.DataFrame({'Actual': y_test_nb, 'Predicted': y_pred_nb})
            st.write('### Naive Bayes Results:')
            st.write(results_nb)

            # Confusion Matrix
            st.write('### Confusion Matrix:')
            confusion_matrix_nb = pd.crosstab(results_nb['Actual'], results_nb['Predicted'], rownames=['Actual'], colnames=['Predicted'])
            st.write(confusion_matrix_nb)

            # Download Naive Bayes Results
            st.write('### Download Naive Bayes Results:')
            st.write('Download the Naive Bayes results as a CSV file.')
            st.markdown(get_table_download_link(results_nb), unsafe_allow_html=True)

        else:
            st.warning('Please select both target and feature columns.')

    # K-Means Clustering
    st.header('K-Means Clustering')
    st.write("""
        Please select two columns for clustering and visualize the results using a scatter plot.
    """)
    clustering_columns_km = st.multiselect('Select Clustering Columns:', cleaned_data.columns)

    # Select the number of clusters for K-Means
    num_clusters_km = st.slider('Select Number of Clusters:', min_value=2, max_value=10, value=2)

    if st.button('Apply K-Means Clustering'):
        if len(clustering_columns_km) == 2:
            # Extract selected columns for clustering
            X_cluster_km = cleaned_data[clustering_columns_km]

            # Create and train the K-Means model with the selected number of clusters
            model_kmeans = KMeans(n_clusters=num_clusters_km, random_state=42)
            cleaned_data['Cluster'] = model_kmeans.fit_predict(X_cluster_km)

            # Visualize clustering using scatter plot
            fig_km = px.scatter(cleaned_data, x=clustering_columns_km[0], y=clustering_columns_km[1], color='Cluster',
                                title=f'K-Means Clustering Results with {num_clusters_km} Clusters')
            st.plotly_chart(fig_km)

            # Display the clustered data
            st.write(cleaned_data.head())

            # Download K-Means Clustering Results
            st.write('### Download K-Means Clustering Results:')
            st.write('Download the K-Means clustering results as a CSV file.')
            st.markdown(get_table_download_link(cleaned_data[['Cluster'] + clustering_columns_km]), unsafe_allow_html=True)

        else:
            st.warning('Please select exactly two clustering columns for visualization.')

    # Apriori Algorithm
    st.header('Apriori Algorithm')
    st.write("""
        Please select the columns for association rule mining using Apriori.
    """)
    apriori_columns = st.multiselect('Select Apriori Columns:', cleaned_data.columns)

    if st.button('Apply Apriori Algorithm'):
        if apriori_columns:
            # Convert selected columns to boolean values (0 or 1)
            data_apriori = cleaned_data[apriori_columns].applymap(lambda x: 1 if x else 0)

            # Apply Apriori algorithm
            frequent_itemsets = apriori(data_apriori, min_support=0.1, use_colnames=True)
            rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.7)

            # Display the generated rules
            st.write('### Frequent Itemsets:')
            st.write(frequent_itemsets)

            st.write('### Association Rules:')
            st.write(rules)

            # Visualize Association Rules
            st.write('### Association Rules Visualization:')
            fig_association = px.scatter(rules, x='support', y='confidence', color='lift',
                                        title='Association Rules Visualization')
            st.plotly_chart(fig_association)

            # Download Apriori Results
            st.write('### Download Apriori Results:')
            st.write('Download the Apriori results as a CSV file.')
            st.markdown(get_table_download_link(rules), unsafe_allow_html=True)

        else:
            st.warning('Please select at least one column for Apriori algorithm.')

# Function to create a download link for a DataFrame as a CSV file
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download CSV File</a>'
    return href

# Include this function call in your main() function where appropriate.
classification_page()
