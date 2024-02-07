import base64
import pandas as pd
from io import BytesIO
import streamlit as st


def export_error_report(master_error_dict, file_name):
    # Convert the master error dictionary into a DataFrame
    error_df = pd.DataFrame.from_dict(master_error_dict, orient='index').T

    # Export to Excel
    towrite = BytesIO()
    error_df.to_excel(towrite, index=False, header=True, engine='xlsxwriter')
    towrite.seek(0)

    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="error_report_{file_name}.xlsx">Download Error Report</a>'
    st.markdown(href, unsafe_allow_html=True)


def export_error_summary(master_error_dict, file_name):
    # Creating a DataFrame for the error counts
    error_count_df = pd.DataFrame({
        "Description": master_error_dict.keys(),
        "Error Count": [len(value) for value in master_error_dict.values()]
    })

    # Export to Excel
    towrite = BytesIO()
    error_count_df.to_excel(towrite, index=False,
                            header=True, engine='xlsxwriter')
    towrite.seek(0)

    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="error_summary_{file_name}.xlsx">Download Error Summary</a>'
    st.markdown(href, unsafe_allow_html=True)


def export_dataframe_to_excel(dataframe, file_name):
    # Export the DataFrame to Excel
    towrite = BytesIO()
    dataframe.to_excel(towrite, index=False, header=True, engine='xlsxwriter')
    towrite.seek(0)

    # Encode the Excel file in base64
    b64 = base64.b64encode(towrite.read()).decode()

    # Create a download link for the Excel file
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}.xlsx">Download {file_name}</a>'

    st.markdown(href, unsafe_allow_html=True)
