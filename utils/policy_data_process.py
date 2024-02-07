import streamlit as st
import pandas as pd
import numpy as np
from utils.table_display import display_table
from utils.file_upload import upload_and_read_file, upload_and_read_large_file
from utils.chart_display import display_charts
import os
from utils.excel_exporter import export_dataframe_to_excel


def process_data(data):
    # Converting the 'PAYMENT_DATE' column to a datetime format
    data['PAYMENT_DATE'] = pd.to_datetime(
        data['PAYMENT_DATE'], errors='coerce')

    # Handling potential NaN values by dropping rows where 'PAYMENT_DATE' is NaT
    data = data.dropna(subset=['PAYMENT_DATE'])

    # Extracting only the date part from the 'PAYMENT_DATE' column
    data['PAYMENT_DATE'] = data['PAYMENT_DATE'].dt.date

    # Sorting the data again by 'POL_NUMBER' in ascending order, and then by 'PAYMENT_DATE' in ascending order
    sorted_data = data.sort_values(
        by=['POL_NUMBER', 'PAYMENT_DATE'], ascending=[True, True])

    # Creating a new dataset with only the 'POL_NUMBER', 'AMOUNT', and 'PAYMENT_DATE' columns
    sorted_data = sorted_data[['POL_NUMBER', 'AMOUNT', 'PAYMENT_DATE']]

    # Displaying the sorted data
    # display_table(sorted_data, "sorted_data")

    # Creating a new dataset with unique 'POL_NUMBER' and the corresponding lowest 'PAYMENT_DATE'
    unique_pol_number_dataset = sorted_data.groupby('POL_NUMBER').agg(
        LOWEST_PAYMENT_DATE=('PAYMENT_DATE', 'min')
    ).reset_index()

    # Displaying the unique POL_NUMBER dataset
    # display_table(unique_pol_number_dataset, "unique_pol_number_dataset")

    return sorted_data, unique_pol_number_dataset


def start_date_process(policy_data, unique_pol_number_dataset):
    # Renaming the POLICY_NUMBER column in policy_data to match the unique_pol_number_dataset
    policy_data.rename(columns={'POLICY_NUMBER': 'POL_NUMBER'}, inplace=True)

    # Merging the unique_pol_number_dataset with policy_data on the POL_NUMBER column to get the START_DATE
    unique_pol_number_dataset = unique_pol_number_dataset.merge(
        policy_data[['POL_NUMBER', 'START_DATE']], on='POL_NUMBER', how='left')

    # Converting the START_DATE column to a proper datetime format
    unique_pol_number_dataset['START_DATE'] = pd.to_datetime(
        unique_pol_number_dataset['START_DATE'], errors='coerce')

    # Extracting only the date part from the 'PAYMENT_DATE' column
    unique_pol_number_dataset['START_DATE'] = unique_pol_number_dataset['START_DATE'].dt.date

    return unique_pol_number_dataset


def display_policy_data():
    # Call the utility function to upload and read the file
    data = upload_and_read_file(key='policy_data_1')

    if data is not None:
        sorted_data, unique_pol_number_dataset = process_data(data)

        # Displaying the sorted data
        st.subheader("Sorted Data")
        display_table(sorted_data, "sorted_data_key")

        # Displaying the unique POL_NUMBER dataset
        st.subheader("Unique POL_NUMBER Dataset")
        display_table(unique_pol_number_dataset, "unique_pol_number_key")

        policy_data = upload_and_read_file(key='policy_data_2')

        if policy_data is not None:
            unique_pol_number_with_start_date = start_date_process(
                policy_data, unique_pol_number_dataset)

            # Displaying the first few rows of the merged dataset with the new START_DATE column
            display_table(unique_pol_number_with_start_date,
                          "unique_pol_number_with_start_date")


def process_and_display_data():

    instructions = """
    **Instructions for this Process:**
    - File must be in CSV or Excel format.
    - First Upload All the Columns DataSet, Only Need Columns Details in First Upload
    - Secondly Upload the All the Policy DataSet to Merge with Columns
    - Check If we have any NaN Values in Stats Column of Our Combined DataSet
    - If We have NaN Value on Status Column Upload Third DataSet to Add Status with Policy Number
    - First Check the Policy Number Column Name is Matching with Our Condition
    - Then, Fix the NaN Column Value Issue
    """

    # Display the instructions using Markdown
    st.markdown(instructions)

    # Create a checkbox to ask the user if they want to upload a file
    # is_upload_columns = st.checkbox("Do you want to upload the columns file?")
    local_file_path_1 = '../Policy_App/utils/all_columns.csv'
    local_file_path_2 = '../utils/all_columns.csv'
    all_columns = None

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_file_path = os.path.join(
        script_dir, '..', 'data', 'all_columns.csv')

    if all_columns is None:
        all_columns = pd.read_csv(csv_file_path)
        st.dataframe(all_columns)
    # elif os.path.exists(local_file_path_2):
    #     all_columns = pd.read_csv(local_file_path_2)
    #     st.dataframe(all_columns)
    else:
        st.subheader('Upload All Columns Dataset')
        all_columns = upload_and_read_file(
            key='all_columns', instruction="Please Upload All the Columns DataSet Here.")

    # try:
    #     local_file_path = '../Policy_App/utils/all_columns.csv'
    #     all_columns = pd.read_csv(local_file_path)
    #     st.dataframe(all_columns)
    # except FileNotFoundError:
    #     st.warning("Local columns dataset not found. Please upload it.")
    #     all_columns = None

    # if all_columns is None:
    #     all_columns = upload_and_read_file(
    #         key='all_columns', instruction="Please Upload All the Columns DataSet Here.")
    st.subheader('Upload Data Extraction Full Report')
    input_data = upload_and_read_large_file(
        key='input_data', instruction="Please Upload the Input DataSet")

    if all_columns is not None and input_data is not None:
        # Getting the columns from both datasets
        columns_new_csv_data = set(all_columns.columns)
        columns_csv_data = set(input_data.columns)

        # Finding the non-matched columns
        non_matched_columns_new_csv_data = columns_new_csv_data - columns_csv_data
        non_matched_columns_csv_data = columns_csv_data - columns_new_csv_data

        # Displaying the non-matched columns
        st.write("Non-matched columns in the new CSV data:",
                 non_matched_columns_new_csv_data)
        st.write("Non-matched columns in the original CSV data:",
                 non_matched_columns_csv_data)

        # Renaming the specified columns in the input_data DataFrame
        input_data_renamed = input_data.rename(columns={
            'MEDREM_PLAN_NAME': 'MEDREM3_PLAN_NAME',
            'SNO': 'NEXT'
        })

        combined_data = pd.concat(
            [all_columns, input_data_renamed], axis=0, ignore_index=True, join="outer")

        # # Displaying the first few rows of the combined dataset
        # st.dataframe(combined_data.head())
        # first_25000_rows = input_data.head(25000)
        # csv_file = first_25000_rows.to_csv(index=False).encode()
        # st.download_button(label="Download CSV File", data=csv_file,
        #                    file_name="input_1_25000_rows.csv", mime="text/csv")

        # Checking and counting NaN values in the 'Status' column
        nan_status_count = pd.isna(combined_data['Status']).sum()
        number_of_rows = combined_data.shape[0]

        st.write(
            f"This Dataset contains {number_of_rows} rows.")
        st.write(
            f"The 'Status' column contains {nan_status_count} NaN values.")

        st.subheader('Upload FYL Dataset')
        status_data = upload_and_read_large_file(
            key='status_data', instruction="Please Upload the DataSet for Status Field Changes")

        if status_data is not None:
            # Assuming 'status_data' contains the necessary columns 'POLICY_NUMBER' and 'Status'
            status_mapping = dict(
                zip(status_data['POLICY_NUMBER'], status_data['Status']))

            # Updating the Status column in the existing CSV data based on the mapping
            combined_data['Status'] = combined_data['POLNUMBER'].astype(
                int).map(status_mapping)

            st.write("Updated DataSet with Status Column Data.")
            # Previewing the updated CSV data
            # st.dataframe(combined_data.head())
            # Extract the first 25,000 rows from the combined_data DataFrame

            # # Merge the extracted rows with the status_data DataFrame on the POLNUMBER and POLICY_NUMBER columns
            # merged_data = first_25000_rows.merge(
            #     status_data, left_on='POLNUMBER', right_on='POLICY_NUMBER', how='inner')

            # # Create a new DataFrame with the same POLNUMBER values
            # new_data_with_same_polnumber = merged_data[merged_data['POLNUMBER']
            #                                            == merged_data['POLICY_NUMBER']]

            # # Display the new DataFrame
            # st.dataframe(new_data_with_same_polnumber)

            # # Optional: Save the new DataFrame to a CSV file
            # # new_data_with_same_polnumber.to_csv(
            # #     "new_data_with_same_polnumber.csv", index=False)

            # # first_25000_rows = status_data.head(25000)
            # csv_file = new_data_with_same_polnumber.to_csv(
            #     index=False).encode()
            # st.download_button(label="Download CSV File", data=csv_file,
            #                    file_name="input_2_25000_rows.csv", mime="text/csv")
            # Checking and counting NaN values in the 'Status' column
            nan_status_count = pd.isna(combined_data['Status']).sum()
            number_of_rows = combined_data.shape[0]

            # Filter rows with NaN values in the 'Status' column and create a new dataset
            nan_status_rows = combined_data[pd.isna(combined_data['Status'])]

            # Remove rows with NaN values in the 'Status' column from the original dataset
            # combined_data = combined_data.dropna(subset=['Status'])

            st.write(
                f"This Dataset contains {number_of_rows} rows.")
            st.write(
                f"The 'Status' column contains {nan_status_count} NaN values.")
            # if nan_status_count > 0:
            #     combined_data['Status'].fillna('Active', inplace=True)
            #     # nan_status_rows = combined_data[pd.isna(
            #     #     combined_data['Status'])]
            #     # st.dataframe(nan_status_rows)
            #     # display_charts(combined_data)
            #     return combined_data
            # else:
            #     # display_charts(combined_data)
            #     return combined_data

            filtered_data = combined_data[combined_data['Status'].isin(
                ["Active", "Paidup", "Tech"])]
            display_table(filtered_data, "combined_data_12")
            display_table(nan_status_rows, "Nan Values in Status")
            export_dataframe_to_excel(nan_status_rows, "NanStatusData")
            return combined_data, filtered_data
