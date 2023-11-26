# visualisation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Access the uploaded dataset from the Streamlit session state
uploaded_data = st.session_state.get('uploaded_data', None)

# Check if data is uploaded
if uploaded_data is not None:
    st.title('Interactive Visualization')

    st.write("""
    This page allows you to create interactive plots based on the dataset you uploaded earlier. 
    Choose two axes from the dataset, select one or more plot types, and customize additional options.
    """)

    # Selecting Axes
    st.sidebar.subheader('Select Axes:')
    x_axis = st.sidebar.selectbox('X-Axis:', uploaded_data.columns)
    y_axis = st.sidebar.selectbox('Y-Axis:', uploaded_data.columns)

    # Selecting Plot Types
    st.sidebar.subheader('Select Plot Types:')
    selected_plot_types = st.sidebar.multiselect('Plot Types:', ['Scatter Plot', 'Line Chart', 'Bar Chart', 'Box Plot', 'Violin Plot', 'Bubble Chart', 'Surface Plot', 'Heatmap'])

    # Additional Options
    st.sidebar.subheader('Additional Options:')
    dimension = st.sidebar.selectbox('Dimension:', ['2D', '3D'])
    show_regression_line = st.sidebar.checkbox('Show Regression Line')
    regression_line_color = st.sidebar.color_picker('Regression Line Color', '#FF0000') if show_regression_line else None
    color_by = st.sidebar.selectbox('Color By:', [None] + uploaded_data.columns.tolist())
    size_by = st.sidebar.selectbox('Size By:', [None] + uploaded_data.columns.tolist())

    # Creating Interactive Plots
    if st.sidebar.button('Generate Plots'):
        st.header('Interactive Plots')

        for plot_type in selected_plot_types:
            st.subheader(f'{dimension} {plot_type}')

            if dimension == '2D':
                if plot_type == 'Heatmap':
                    fig = px.imshow(uploaded_data, x=uploaded_data.columns, y=uploaded_data.index, color_continuous_scale='viridis')
                else:
                    fig = px.scatter(uploaded_data, x=x_axis, y=y_axis, hover_name=uploaded_data.index,
                                     trendline='ols' if show_regression_line else None, color=color_by, size=size_by)

                    # Customize regression line appearance
                    if show_regression_line and regression_line_color:
                        fig.data[1].update(line=dict(color=regression_line_color))

            elif dimension == '3D':
                z_axis = st.sidebar.selectbox('Z-Axis:', uploaded_data.columns)
                fig = go.Figure()

                if plot_type == 'Scatter Plot':
                    fig.add_trace(go.Scatter3d(x=uploaded_data[x_axis], y=uploaded_data[y_axis], z=uploaded_data[z_axis],
                                               mode='markers', marker=dict(size=uploaded_data[size_by], color=uploaded_data[color_by]),
                                               text=uploaded_data.index, name='Data Points'))

                if show_regression_line:
                    regression_line = px.get_trendline_results(px.scatter(uploaded_data, x=x_axis, y=y_axis, trendline='ols'))
                    slope, intercept = regression_line['px_fit_results'][0].params
                    line = go.Scatter3d(x=uploaded_data[x_axis], y=uploaded_data[y_axis], z=slope * uploaded_data[x_axis] + intercept,
                                       mode='lines', line=dict(color=regression_line_color), name='Regression Line')
                    fig.add_trace(line)

                fig.update_layout(scene=dict(xaxis_title=x_axis, yaxis_title=y_axis, zaxis_title=z_axis),
                                  margin=dict(l=0, r=0, b=0, t=0))

            st.plotly_chart(fig)

            st.caption(f'{dimension} {plot_type} showing the relationship between {x_axis}, {y_axis}, and {z_axis if dimension == "3D" else ""}.')
else:
    st.warning('Please upload a CSV file in the Upload page.')
