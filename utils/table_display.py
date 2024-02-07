import streamlit as st
import pandas as pd

def display_table(data,unique_key, rows_per_page=10):
    # # Calculate the number of pages
    # num_pages = len(data) // rows_per_page
    # if len(data) % rows_per_page != 0:
    #     num_pages += 1

    # # Slider or other widget to choose the page number
    # page_num = st.slider("Choose a page:", min_value=1, max_value=num_pages, value=1)

    # # Slice the DataFrame to show the selected page
    # start_idx = (page_num - 1) * rows_per_page
    # end_idx = start_idx + rows_per_page
    # page_data = data.iloc[start_idx:end_idx]

    # # Convert the sliced DataFrame to HTML
    # html_page_data = page_data.to_html(index=False)

    # # Define custom CSS styles
    # custom_css = """
    # <style>
    #     table {
    #         width: 100%;
    #         border-collapse: collapse;
    #     }
    #     th, td {
    #         border: 1px solid black;
    #         padding: 8px;
    #         text-align: left;
    #     }
    #     tr:nth-child(even) {
    #         background-color: #f2f2f2;
    #     }
    #     th {
    #         background-color: #4CAF50;
    #         color: white;
    #     }
    # </style>
    # """

    # # Combine the custom CSS with the HTML table
    # html_content = custom_css + html_page_data

    # # Display the HTML content using st.write or st.markdown
    # st.write(html_content, unsafe_allow_html=True)

    # Number of rows to show per page
    # rows_per_page = 15  # Updated to 15 rows per page

    # Calculate the number of pages
    num_pages = len(data) // rows_per_page
    if len(data) % rows_per_page != 0:
        num_pages += 1

    # Slider or other widget to choose the page number
    page_num = st.slider("Choose a page:", min_value=1, max_value=num_pages, value=1,key=unique_key)


    # Slice the DataFrame to show the selected page
    start_idx = (page_num - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    page_data = data.iloc[start_idx:end_idx]

    # Display the sliced DataFrame with st.dataframe
    st.data_editor(
    page_data,
    column_config={
        "widgets": st.column_config.Column(
            width="medium",
        )
    },
    hide_index=True,
)
    # st.dataframe(page_data)

def display_table_with_formatting(df, column_types):
    # Iterate through the specified columns and data types
    for column_name, dtype in column_types.items():
        # Check if the column exists in the DataFrame
        if column_name in df.columns:
            # Convert the column to the specified data type
            if dtype == 'datetime':
                df[column_name] = pd.to_datetime(df[column_name])
                # Optional: Format the datetime column (adjust as needed)
                df[column_name] = df[column_name].dt.strftime("%D %b %Y, %I:%M %p")
            else:
                df[column_name] = df[column_name].astype(dtype)

    # Display the DataFrame in Streamlit
    st.dataframe(df)