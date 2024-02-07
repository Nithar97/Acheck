import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


def get_image_download_link(img, filename):
    """Generate a link to download the image"""
    buffered = io.BytesIO()
    img.savefig(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download as PNG</a>'
    return href


def display_charts(data):

    # Check if the selected_charts state exists, if not, initialize it
    if 'selected_charts' not in st.session_state:
        st.session_state.selected_charts = []

    # Filtering columns that contain at least one non-NaN value
    valid_columns = [col for col in data.columns if data[col].notna().any()]

    selected_column = st.selectbox(
        "Select a column to visualize:", options=valid_columns
    )

    chart_library = 'Streamlit'

    chart_library = st.selectbox(
        "Select a chart library:",
        options=["Streamlit", "Matplotlib/Seaborn"],
    )

    chart_type = st.selectbox(
        "Select a chart type:",
        options=[
            "Line Chart",
            "Bar Chart",
            "Histogram",
            "Scatter Plot",
            "Box Plot",
        ],
    )

    if st.button("Add Chart"):
        # Append the selected chart to the session state
        st.session_state.selected_charts.append(
            (selected_column, chart_type, chart_library))

    # # Iterate through the selected charts and display them
    # for selected_column, chart_type in st.session_state.selected_charts:
    #     st.subheader(f"{chart_type} for {selected_column}")
    #     st.write(f"Column: {selected_column}, Chart Type: {chart_type}")

    #     fig, ax = plt.subplots()
    #     if chart_type == "Line Chart":
    #         st.line_chart(data[selected_column])
    #     elif chart_type == "Bar Chart":
    #         st.bar_chart(data[selected_column])
    #     elif chart_type == "Histogram":

    #         sns.histplot(data[selected_column], kde=False, ax=ax)
    #         st.pyplot(fig)
    #     elif chart_type == "Scatter Plot":
    #         other_column = st.selectbox(
    #             f"Select another column to compare with {selected_column}:",
    #             options=[col for col in data.columns if col != selected_column],
    #         )
    #         sns.scatterplot(x=selected_column,
    #                         y=other_column, data=data, ax=ax)
    #         st.pyplot(fig)
    #     elif chart_type == "Box Plot":
    #         sns.boxplot(x=data[selected_column], ax=ax)
    #         st.pyplot(fig)

    #     # Provide a link to download the plot as PNG
    #     st.markdown(get_image_download_link(
    #         fig, f"{selected_column}_{chart_type}.png"), unsafe_allow_html=True)
   # Iterate through the selected charts and display them
    for selected_column, chart_type, chart_library in st.session_state.selected_charts:
        st.subheader(
            f"{chart_type} for {selected_column} using {chart_library}")

        if chart_library == "Streamlit":
            if chart_type == "Line Chart":
                st.line_chart(data[selected_column])
            elif chart_type == "Bar Chart":
                st.bar_chart(data[selected_column])
        else:  # Matplotlib/Seaborn
            fig, ax = plt.subplots()

            if chart_type == "Histogram":
                sns.histplot(data[selected_column], kde=False, ax=ax)
            elif chart_type == "Scatter Plot":
                other_column = st.selectbox(
                    f"Select another column to compare with {selected_column}:",
                    options=[col for col in data.columns if col !=
                             selected_column],
                )
                sns.scatterplot(x=selected_column,
                                y=other_column, data=data, ax=ax)
            elif chart_type == "Box Plot":
                sns.boxplot(x=data[selected_column], ax=ax)

            st.pyplot(fig)

            # Provide a link to download the plot as PNG
            st.markdown(get_image_download_link(
                fig, f"{selected_column}_{chart_type}.png"), unsafe_allow_html=True)
