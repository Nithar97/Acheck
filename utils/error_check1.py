import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling

from utils.file_upload import upload_and_read_file
from utils.policy_data_process import process_and_display_data
from utils.validations import run_premium_validations, run_custom_validations, run_age_validations, run_plan_terms_validations, run_cancer_validations, run_child_validations
from utils.excel_exporter import export_error_report, export_error_summary


def error_check1(valuation_date):
    filtered_data, status_data = process_and_display_data()
    if filtered_data is not None:
        # columns_to_display = ['PROPOSALNUMBER', 'POLNUMBER', 'PLAN',	"TERM", "MODE", 'COMMDATE', 'GENDER1',
        #                       'GENDER2', 'DOB1', 'DOB2', 'AGE1', 'AGE2', 'SUMASSURED', 'INSTPREMIUM', 'BRANCH', 'Status']
        # df_profile = filtered_data[columns_to_display]

        # pr = ProfileReport(df_profile, explorative=True)
        # st.header('**Pandas Profiling Report**')
        # st_profile_report(pr)

        # pr = filtered_data.profile_report()
        # st_profile_report(pr)
        # Generate the profile report
        # Select specific columns to display

        # profile = df_profile.profile_report()
        # st.write('## Profile Report')
        # st.components.v1.html(profile.to_html(), height=1000)

        # Initialize session_state variables if they don't exist
        if 'has_clicked' not in st.session_state:
            st.session_state.has_clicked = False

        if st.button("Run All Validations and Generate Reports"):
            st.session_state.has_clicked = True

        # Check if the button was clicked in any previous run
        if st.session_state.has_clicked:
            # # if st.button("Run Custom Validations"):

            # combined_errors_count, error_dict = run_premium_validations(
            #     filtered_data)
            # st.write(error_dict)
            # st.write(combined_errors_count)

            # combined_errors_count, error_dict = run_age_validations(
            #     filtered_data, valuation_date)
            # st.write(error_dict)
            # st.write(combined_errors_count)

            # combined_errors_count, error_dict = run_plan_terms_validations(
            #     filtered_data)
            # st.write(error_dict)
            # st.write(combined_errors_count)

            # combined_errors_count, error_dict = run_cancer_validations(
            #     filtered_data)
            # st.write(error_dict)
            # st.write(combined_errors_count)
            # Initialize a master error dictionary
            master_error_dict = {}

            # Run all validations and merge their outputs into master_error_dict
            for validation_function in [run_custom_validations, run_premium_validations, run_age_validations, run_plan_terms_validations, run_cancer_validations, run_child_validations]:
                if validation_function == run_age_validations:
                    combined_errors_count, error_dict = validation_function(
                        filtered_data, valuation_date)
                else:
                    combined_errors_count, error_dict = validation_function(
                        filtered_data)

                # Merge error_dict into master_error_dict
                master_error_dict.update(error_dict)

            master_error_dict = dict(sorted(master_error_dict.items()))
            st.write(master_error_dict)

            exceptions_data = upload_and_read_file(
                key='exceptions', instruction="Please Upload the Exceptions File.")

            if exceptions_data is None:
                st.warning("Failed to upload Exceptions. Please try again.")
                return 0, {}

            if exceptions_data is not None:
                removed_data_dict = {key: []
                                     for key in master_error_dict.keys()}
                unique_ids = exceptions_data['Unique ID']
                for uid in unique_ids:
                    for key, values in master_error_dict.items():
                        for value in values:
                            if str(uid) in value:
                                master_error_dict[key].remove(value)
                                removed_data_dict[key].append(value)

                # remove empty keys from removed_data_dict
                removed_data_dict = {k: v for k,
                                     v in removed_data_dict.items() if v}

                st.write(removed_data_dict)

                export_error_report(master_error_dict, valuation_date)
                export_error_summary(master_error_dict, valuation_date)
