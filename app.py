import streamlit as st
from datetime import datetime
from io import BytesIO
import base64
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling

from utils.file_upload import upload_and_read_file
from utils.table_display import display_table
from utils.table_display import display_table_with_formatting
from utils.policy_data_process import process_data, start_date_process, process_and_display_data, display_policy_data
from utils.validations import run_premium_validations, run_custom_validations, run_age_validations, run_plan_terms_validations, run_cancer_validations, run_child_validations
from utils.excel_exporter import export_error_report, export_error_summary
from checks.page_1 import error_check1

# Set the page configuration (only once, at the beginning of the script)
st.set_page_config(
    page_title="Actuarial Application",
    # layout="wide"  # Optional: set the layout to "wide"
)


def main():
    # Display the logo
    st.image("./image/logo.png", width=50, use_column_width="auto")
    st.title("Actuarial Data Extraction Check WebApplication")

    # Text input for the user to enter a date
    user_input_date = st.text_input(
        'Enter a date in DD-MM-YYYY format:')
    # Check if the user input is not empty and matches the desired format
    if user_input_date:
        try:
            valuation_date = datetime.strptime(user_input_date, '%d-%m-%Y')
            st.session_state.global_valuation_date = pd.to_datetime(
                valuation_date).date()
        except ValueError:
            st.warning("Please enter a valid date in DD-MM-YYYY format.")
            return
    else:
        st.warning("Please enter valuation date.")
        return

    error_check1()


if __name__ == "__main__":
    main()
