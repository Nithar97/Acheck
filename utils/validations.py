import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, date
import os
from dateutil.relativedelta import relativedelta


from utils.file_upload import upload_and_read_file, upload_and_read_large_file


def validation_84(dataframe, combined_errors_count, error_dict):
    validation_message = "DOB1 is empty"

    # Check if the DOB1 column is empty
    validation_errors = dataframe['DOB1'].isna()

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_85(dataframe, combined_errors_count, error_dict):
    validation_message = "GENDER1 not M or F"

    # Check if the GENDER1 column contains values other than 'M' or 'F'
    validation_errors = ~dataframe['GENDER1'].isin(['M', 'F'])

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_86(dataframe, combined_errors_count, error_dict):
    validation_message = "GENDER2 not M,F or empty"

    # Check if the GENDER2 column contains values other than 'M', 'F', or NaN
    validation_errors = ~(dataframe['GENDER2'].isin(
        ['M', 'F']) | dataframe['GENDER2'].isna())

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_87(dataframe, combined_errors_count, error_dict):
    validation_message = "DOB2 or GENDER2 missing"

    # Check if the DOB2 or GENDER2 columns are missing (NaN)
    validation_errors = ~dataframe['DOB2'].isna() & dataframe['GENDER2'].isna(
    ) | dataframe['DOB2'].isna() & ~dataframe['GENDER2'].isna()

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_90(dataframe, combined_errors_count, error_dict):
    validation_message = "Age at maturity exceed 80 years"

    # Check if the Age + Term is greater than 80 and Plan is not equal to 30
    validation_errors = (
        (dataframe['AGE1'] + dataframe['TERM']) > 80) & (dataframe['PLAN'] != 30)

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_131(dataframe, combined_errors_count, error_dict):
    validation_message = "Current age of main life exceeds 65 years in plan 20 MyFund or main life date of birth missing"

    # Check if the Plan column value is 20
    plan_condition = dataframe['PLAN'] == 20
    valuation_date = st.session_state.global_valuation_date
    # # Check if the Terms column value is either 3 or 5
    # # Convert the dates in COLUMN_1 to datetime
    dob_1_values = pd.to_datetime(
        dataframe['DOB1'], format="%d/%m/%Y", errors='coerce')

    # # Replace None/NaT values with a minimum date for comparison
    dob_values = dob_1_values.fillna(np.datetime64('1700-01-01'))

    # # # Get the maximum date for each row between COLUMN_1 and COLUMN_2
    # # dob_values = np.where(dob_1_values >= dob_2_values,
    # #                           dob_1_values, dob_2_values)
    # # dob_values = pd.Series(dob_values)
    # # Convert dob_values to a Series of datetime.date objects
    # dob_dates = dob_values.dt.date

    # # Calculate the ages in days based on the user-entered date
    # ages_in_days = [(valuation_date - dob_date).days if pd.notna(dob_date)
    #                 else None for dob_date in dob_dates]

    # # Convert ages in days to ages in years
    # ages = np.array([age_in_days / 365.25 if age_in_days is not None
    #                  else 0 for age_in_days in ages_in_days])
    # Get the maximum date for each row between COLUMN_1 and COLUMN_2
    # dob_values = np.maximum(dob_1_values, dob_2_values)

    # Convert numpy array to Pandas Series
    dob_values = pd.Series(dob_values)

    # Function to calculate age using python-dateutil
    def calculate_age(dob, current_date):
        if pd.isna(dob):
            return None
        dob = pd.to_datetime(dob).date()
        current_date = pd.to_datetime(current_date).date()
        age = relativedelta(current_date, dob)
        return age.years

    # Assuming valuation_date is a datetime.date or datetime.datetime object
    valuation_date = pd.to_datetime(valuation_date)

    # Calculate ages using the calculate_age function
    ages = dob_values.apply(lambda dob: calculate_age(dob, valuation_date))

    # Replace NaN values with 0 or any other desired default value
    ages = ages.fillna(0)

    # Assuming 'AGE_AS_AT_DOV' is the name of the age limit column
    age_limit = 65

    # Check if the calculated age is greater than the age limit
    age_errors = ages >= age_limit

    # Combine both conditions
    age_errors = pd.Series(age_errors).astype(bool)
    plan_condition = pd.Series(plan_condition).astype(bool)

    validation_errors = plan_condition & age_errors

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_150(dataframe, combined_errors_count, error_dict):
    validation_message = "Policy term of plan 39 PrivilegeLife is less than premium payment term"

    # Check if the Plan column value is 39
    plan_condition = dataframe['PLAN'] == 39

    terms_condition = dataframe['TERM'] < dataframe['PREM_PAYING_TERM']

    # Combine both conditions
    validation_errors = plan_condition & terms_condition

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_151(dataframe, combined_errors_count, error_dict):
    validation_message = "Duplicate records"

    # Check for duplicate values in the POLNUMBER column
    validation_errors = dataframe['POLNUMBER'].duplicated(keep=False)

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_152(dataframe, combined_errors_count, error_dict):
    validation_message = "Blank plan number"

    # Check if the PLAN column is empty (NaN) or zero
    validation_errors = dataframe['PLAN'].isna() | (dataframe['PLAN'] == 0)

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_177(dataframe, combined_errors_count, error_dict):
    validation_message = "Supreme Health Max (MED-REM4) deductible amount not valid"

    validate_1 = dataframe['MEDREM_COVER_CODE'] == 'MED-REM4'
    dataframe['MEDREM4_DEDUCT_DISC_OPT'] = pd.to_numeric(
        dataframe['MEDREM4_DEDUCT_DISC_OPT'], errors='coerce').fillna(0).astype(int)
    validate_2 = ~dataframe['MEDREM4_DEDUCT_DISC_OPT'].isin(
        [0, 50000, 100000, 150000, 200000])

    validation_errors = validate_1 & validate_2

    if validation_errors.any():
        st.write(dataframe[['MEDREM4_DEDUCT_DISC_OPT', 'POLNUMBER']])

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_178(dataframe, combined_errors_count, error_dict):
    validation_message = "Spouse age at entry for MED-REM4 (Supreme Health Max) maternity benefit exceed 42 years"

    validate_1 = dataframe['MEDREM_COVER_CODE'] == 'MED-REM4'
    validate_2 = dataframe['MEDREM4_SP_MATER_COVER_OPT'] == 'YES'
    validate_3 = dataframe['AGE2'] > 42

    validation_errors = validate_1 & validate_2 & validate_3

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def validation_179(dataframe, combined_errors_count, error_dict):
    validation_message = "Main life at entry for MED-REM4 (Supreme Health Max) maternity benefit exceed 42 years"

    validate_1 = dataframe['MEDREM_COVER_CODE'] == 'MED-REM4'
    validate_2 = dataframe['MEDREM4_LA_MATER_COVER_OPT'] == 'YES'
    validate_3 = dataframe['AGE1'] > 42

    validation_errors = validate_1 & validate_2 & validate_3

    return build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict)


def run_custom_validations(dataframe):
    validations = [validation_84, validation_85, validation_86,
                   validation_87, validation_90, validation_131, validation_150, validation_151, validation_152, validation_177, validation_178, validation_179]

    error_dict = {}
    combined_errors_count = 0

    for validation in validations:
        combined_errors_count, error_dict = validation(
            dataframe, combined_errors_count, error_dict)

    return combined_errors_count, error_dict

# def run_custom_validations(dataframe):
#     # List of all validation functions
#     validations = [validation1, validation2,
#                    validation_3, validation_4, validation_5, validation_6, validation_7]

#     # Dictionary to store the error arrays with validation function names as keys
#     error_dict = {}

#     # Initialize combined errors as a Series filled with False
#     combined_errors_count = 0

#     # Run all validations and combine the errors using logical OR
#     for validation in validations:
#         total_errors, error_array = validation(dataframe)
#         combined_errors_count += total_errors

#         # Add the error array to the dictionary with the validation function name as the key
#         # error_dict[validation.__name__] = error_array
#         # Converting error_array to a NumPy array
#         # error_dict[validation.__name__] = np.array(error_array)
#         error_dict[validation.__name__] = error_array

#     return combined_errors_count, error_dict


def run_premium_validations(dataframe):
    # st.subheader('Premium Validations')
    # validation_rules = upload_and_read_file(
    #     key='all_columns_validation_check', instruction="Please Upload All the Columns DataSet Here.")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_file_path = os.path.join(
        script_dir, '..', 'data', 'Validation_Check_Premium.csv')

    validation_rules = pd.read_csv(csv_file_path)

    if validation_rules is None:
        st.warning("Failed to upload validation rules. Please try again.")
        return 0, {}

    error_dict = {}
    combined_errors_count = 0

    for _, row in validation_rules.iterrows():
        validation_message = row['VALIDATION_MESSAGE']

        validation1_errors = dataframe[row['COLUMN_1']].fillna(0)
        if pd.notnull(row['COLUMN_2']):
            validation1_errors += dataframe[row['COLUMN_2']].fillna(0)
        validation1_errors = np.greater(validation1_errors, 0)

        validation2_errors = dataframe[row['COLUMN_3']].fillna(0)
        if pd.notnull(row['COLUMN_4']):
            validation2_errors += dataframe[row['COLUMN_4']].fillna(0)
        validation2_errors = np.equal(validation2_errors, 0)

        if pd.notnull(row['COLUMN_5']):
            acceptable_plans = [int(x) for x in row['PLANS'].split(',') if x]
            validation3_errors = ~dataframe[row['COLUMN_5']].isin(
                acceptable_plans)
            combined_errors = validation1_errors & validation2_errors & validation3_errors
        else:
            combined_errors = validation1_errors & validation2_errors

        combined_errors_count, error_dict = build_error_array_and_dict(
            dataframe, combined_errors, row, validation_message, combined_errors_count, error_dict)

    return combined_errors_count, error_dict


def run_age_validations(dataframe, valuation_date):
    # st.subheader('Age Validations')
    # validation_rules = upload_and_read_file(
    #     key='all_columns_validation_age_check_1', instruction="Please Upload All the Columns DataSet Here.")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_file_path = os.path.join(
        script_dir, '..', 'data', 'Validation_Check_Age.csv')

    validation_rules = pd.read_csv(csv_file_path)

    if validation_rules is None:
        st.warning("Failed to upload validation rules. Please try again.")
        return 0, {}

    error_dict = {}
    combined_errors_count = 0

    # Convert valuation_date to a datetime.date object
    valuation_date = pd.to_datetime(valuation_date).date()

    for _, row in validation_rules.iterrows():
        validation_message = row['VALIDATION_MESSAGE']

        # # Get the column name from COLUMN_1 and COLUMN_2
        # dob_column = row['COLUMN_1']
        # value_column = row['COLUMN_2']

        # # Convert the dates in the specified column to datetime
        # dob_values = pd.to_datetime(
        #     dataframe[dob_column], format="%d/%m/%Y", errors='coerce')

        # Convert the dates in COLUMN_1 to datetime
        dob_1_values = pd.to_datetime(
            dataframe[row['COLUMN_1']], format="%d/%m/%Y", errors='coerce')

        # Convert the dates in COLUMN_2 to datetime, if it exists
        if pd.notnull(row.get('COLUMN_2')):
            dob_2_values = pd.to_datetime(
                dataframe[row['COLUMN_2']], format="%d/%m/%Y", errors='coerce')
        else:
            dob_2_values = pd.Series([np.datetime64('NaT')]*len(dataframe))

        # # Replace None/NaT values with a minimum date for comparison
        # dob_1_values = dob_1_values.fillna(np.datetime64('1700-01-01'))
        # dob_2_values = dob_2_values.fillna(np.datetime64('1700-01-01'))

        # # Get the maximum date for each row between COLUMN_1 and COLUMN_2
        # dob_values = np.where(dob_1_values >= dob_2_values,
        #                       dob_1_values, dob_2_values)
        # dob_values = pd.Series(dob_values)
        # # Convert dob_values to a Series of datetime.date objects
        # dob_dates = dob_values.dt.date

        # # Calculate the ages in days based on the user-entered date
        # ages_in_days = [(valuation_date - dob_date).days if pd.notna(dob_date)
        #                 else None for dob_date in dob_dates]

        # # # Convert ages in days to ages in years
        # ages = np.array([age_in_days / 365.25 if age_in_days is not None
        #                  else 0 for age_in_days in ages_in_days])
        # Assuming dob_1_values and dob_2_values are numpy arrays of datetime64 type

        # Get the maximum date for each row between COLUMN_1 and COLUMN_2
        dob_values = np.maximum(dob_1_values, dob_2_values)

        # Convert numpy array to Pandas Series
        dob_values = pd.Series(dob_values)

        # Function to calculate age using python-dateutil
        def calculate_age(dob, current_date):
            if pd.isna(dob):
                return None
            dob = pd.to_datetime(dob).date()
            current_date = pd.to_datetime(current_date).date()
            age = relativedelta(current_date, dob)
            return age.years

        # Assuming valuation_date is a datetime.date or datetime.datetime object
        valuation_date = pd.to_datetime(valuation_date)

        # Calculate ages using the calculate_age function
        ages = dob_values.apply(lambda dob: calculate_age(dob, valuation_date))

        # Replace NaN values with 0 or any other desired default value
        ages = ages.fillna(0)

        # def calculate_age(dob, valuation_date):
        #     # Ensure dob is a date object
        #     if pd.notna(dob):
        #         # Calculate initial age in years
        #         age = valuation_date.year - dob.year

        #         # Check if we've passed the birth date this year, if not, subtract one year
        #         if (valuation_date.month, valuation_date.day) < (dob.month, dob.day):
        #             age -= 1
        #         return age
        #     else:
        #         return None

        # ages = [calculate_age(dob_date, valuation_date)
        #         for dob_date in dob_dates]

        # Assuming 'AGE_AS_AT_DOV' is the name of the age limit column
        age_limit = row['AGE_AS_AT_DOV']

        # Check if the corresponding values in COLUMN_2 are greater than zero
        # Extract values from COLUMN_3
        value_1 = dataframe[row['COLUMN_3']]

        # For COLUMN_4 and COLUMN_5, handle potential NaNs
        if pd.notnull(row.get('COLUMN_4')):
            value_2 = dataframe[row['COLUMN_4']]
        else:
            value_2 = pd.Series([0]*len(dataframe))

        if pd.notnull(row.get('COLUMN_5')):
            value_3 = dataframe[row['COLUMN_5']]
        else:
            value_3 = pd.Series([0]*len(dataframe))

        # Calculate the maximum value from COLUMN_3, COLUMN_4, and COLUMN_5
        value_condition = np.nanmax(
            np.array([value_1, value_2, value_3]), axis=0)

        validation_status = dataframe['Status'].isin(
            ["Active", "Paidup", "Tech"])
        # value_condition = dataframe[value_column] > 0

        # Check if the calculated age is greater than the age limit
        age_errors = (ages >= age_limit)

        # Check if the date of birth is missing
        # dob_missing_errors = dob_values.isna()
        # if validation_message == "Age of CI rider spouse beneficiary exceeded 70 years or spouse date of birth missing":
        #     st.write(validation_message)
        #     st.write(dataframe[row['COLUMN_1']])
        #     st.write(age_errors)
        #     if pd.notnull(row.get('COLUMN_2')):
        #         st.write(dataframe[row['COLUMN_2']])
        #     st.write(value_condition > 0)
        # Combine all conditions
        # combined_errors = age_errors & value_condition & validation_status
        # Example of type conversion and ensuring compatibility
        age_errors = pd.Series(age_errors).astype(bool)
        value_condition = pd.Series(value_condition).astype(bool)
        validation_status = pd.Series(validation_status).astype(bool)

        # Ensure they are all of the same length
        if len(age_errors) == len(value_condition) == len(validation_status):
            combined_errors = age_errors & value_condition & validation_status
        else:
            # Handle error or mismatch in array lengths
            pass

        combined_errors_count, error_dict = build_error_array_and_dict(
            dataframe, combined_errors, row, validation_message, combined_errors_count, error_dict)

    return combined_errors_count, error_dict


def run_plan_terms_validations(dataframe):
    # st.subheader('Plan & Terms Validations')
    # validation_rules = upload_and_read_file(
    #     key='all_columns_validation_age_check_3', instruction="Please Upload All the Columns DataSet Here.")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_file_path = os.path.join(
        script_dir, '..', 'data', 'Validation_Check_Plan_Term.csv')

    validation_rules = pd.read_csv(csv_file_path)

    if validation_rules is None:
        st.warning("Failed to upload validation rules. Please try again.")
        return 0, {}

    error_dict = {}
    combined_errors_count = 0

    for _, row in validation_rules.iterrows():
        validation_message = row['VALIDATION_MESSAGE']

        if pd.notna(row['COLUMN_1']) and pd.notna(row['COLUMN_2']) and row['COLUMN_1'] in dataframe.columns:
            mask_eq = dataframe[row['COLUMN_1']].isin(
                str(row['COLUMN_2']).split('|'))
        else:
            continue  # skip this iteration as COLUMN_1 or COLUMN_2 is NaN or COLUMN_1 not in dataframe

        if pd.notna(row['COLUMN_4']) and row['COLUMN_4'] in dataframe.columns:
            # Convert the columns to datetime
            date_values_1 = pd.to_datetime(
                dataframe[row['COLUMN_3']], format="%d/%m/%Y", errors='coerce')
            date_values_2 = pd.to_datetime(
                dataframe[row['COLUMN_4']], format="%d/%m/%Y", errors='coerce')

            # Calculate the difference in years
            years_difference = (
                date_values_2 - date_values_1) / np.timedelta64(1, 'Y')

            # Now, you can apply the conditions in COLUMN_6 to years_difference
            if row['COLUMN_6'] == "<>":
                mask = (years_difference != float(
                    row['COLUMN_5'])) & mask_contain
            elif row['COLUMN_6'] == ">":
                mask = years_difference > float(row['COLUMN_5'])
            elif row['COLUMN_6'] == "<":
                mask = years_difference < float(row['COLUMN_5'])
        else:
            if pd.notna(row['COLUMN_3']) and pd.notna(row['COLUMN_5']) and row['COLUMN_3'] in dataframe.columns:
                mask_contain = dataframe[row['COLUMN_3']].isin(
                    str(row['COLUMN_5']).split('|'))
            else:
                mask_contain = pd.Series([False] * len(dataframe))

            if row['COLUMN_6'] == "<>":
                mask = mask_contain
            elif row['COLUMN_6'] == ">":
                mask = dataframe[row['COLUMN_3']] > float(row['COLUMN_5'])
            elif row['COLUMN_6'] == "<":
                mask = dataframe[row['COLUMN_3']] < float(row['COLUMN_5'])

        combined_errors_count, error_dict = build_error_array_and_dict(
            dataframe, mask & mask_eq, row, validation_message, combined_errors_count, error_dict)

    return combined_errors_count, error_dict


def run_cancer_validations(dataframe):
    # st.subheader('Cancer Validations')
    # validation_rules = upload_and_read_file(
    #     key='all_columns_validation_age_check_4', instruction="Please Upload All the Columns DataSet Here.")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_file_path = os.path.join(
        script_dir, '..', 'data', 'Validation_Check_Cancer.csv')

    validation_rules = pd.read_csv(csv_file_path)

    if validation_rules is None:
        st.warning("Failed to upload validation rules. Please try again.")
        return 0, {}

    error_dict = {}
    combined_errors_count = 0

    for _, row in validation_rules.iterrows():
        validation_message = row['VALIDATION_MESSAGE']

        if pd.notna(row['COLUMN_1']) and pd.notna(row['COLUMN_2']) and row['COLUMN_1'] in dataframe.columns:
            mask_contain = dataframe[row['COLUMN_1']].isin(
                str(row['COLUMN_2']).split('|'))
        else:
            mask_contain = pd.Series([False] * len(dataframe))

        if row['COLUMN_3'] == "<>":
            mask = mask_contain
        elif row['COLUMN_3'] == ">":
            mask = dataframe[row['COLUMN_1']] > float(row['COLUMN_2'])
        elif row['COLUMN_3'] == "<":
            mask = dataframe[row['COLUMN_1']] < float(row['COLUMN_2'])

        combined_errors_count, error_dict = build_error_array_and_dict(
            dataframe, mask, row, validation_message, combined_errors_count, error_dict)

    return combined_errors_count, error_dict


def run_child_validations(dataframe):
    # st.subheader('Child Validations')
    # validation_rules = upload_and_read_file(
    #     key='all_columns_validation_age_check_5', instruction="Please Upload All the Columns DataSet Here.")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_file_path = os.path.join(
        script_dir, '..', 'data', 'Validation_Check_Child.csv')

    validation_rules = pd.read_csv(csv_file_path)

    if validation_rules is None:
        st.warning("Failed to upload validation rules. Please try again.")
        return 0, {}

    error_dict = {}
    combined_errors_count = 0

    for _, row in validation_rules.iterrows():
        validation_message = row['VALIDATION_MESSAGE']

        # For values in COLUMN_1 equal to COLUMN_2
        mask_equal = dataframe[row['COLUMN_1']] == row['COLUMN_2']

        # For values in COLUMN_3 not in COLUMN_4
        column_4_values = [int(value)
                           for value in str(row['COLUMN_4']).split('|')]
        # column_4_values = str(row['COLUMN_4']).split('|')
        # st.write(column_4_values)
        mask_not_in = pd.notna(dataframe[row['COLUMN_3']]) & ~dataframe[row['COLUMN_3']].isin(
            column_4_values)

        # Combine the two masks
        mask = mask_equal & mask_not_in

        combined_errors_count, error_dict = build_error_array_and_dict(
            dataframe, mask, row, validation_message, combined_errors_count, error_dict)

    return combined_errors_count, error_dict


def build_error_array_and_dict(dataframe, combined_errors, row, validation_message, combined_errors_count, error_dict):
    error_array = [str(pol_number) + validation_message for pol_number,
                   error in zip(dataframe['POLNUMBER'], combined_errors) if error]

    total_errors = len(error_array)
    combined_errors_count += total_errors
    # error_key = 'validation_' + str(row['VALIDATION_ID'])
    error_key = str(row['VALIDATION_MESSAGE'])
    error_dict[error_key] = error_array

    return combined_errors_count, error_dict


def build_custom_error_array_and_dict(dataframe, validation_errors, validation_message, combined_errors_count, error_dict):
    error_array = [str(pol_number) + validation_message for pol_number,
                   error in zip(dataframe['POLNUMBER'], validation_errors) if error]

    total_errors = len(error_array)
    combined_errors_count += total_errors
    error_key = validation_message
    error_dict[error_key] = error_array

    return combined_errors_count, error_dict
