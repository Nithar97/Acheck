import streamlit as st
import pandas as pd
import chardet


def upload_and_read_file(key, instruction="Please upload a CSV or Excel file", type=["csv", "xlsx"]):

    # Displaying the instruction message
    # st.markdown(f"**{instruction}**")
    uploaded_file = st.file_uploader(instruction, type=type, key=key)

    data = None  # Placeholder for the DataFrame

    if uploaded_file is not None:
        # # Determine the file type and read the file into a Pandas DataFrame
        # if uploaded_file.name.endswith('.csv'):
        #     uploaded_data = pd.read_csv(uploaded_file, chunksize=25000)
        #     output = pd.DataFrame()
        #     for chunk in uploaded_data:
        #         categorical_columns = chunk.select_dtypes(
        #             include=['object', 'category']).columns
        #         st.write(categorical_columns)
        #         data = chunk
        #         break
        try:
            result = chardet.detect(uploaded_file.read())
            uploaded_file.seek(0)  # Reset the file pointer to the beginning
            if uploaded_file.name.endswith('.csv'):
                uploaded_data = pd.read_csv(
                    uploaded_file, chunksize=50000, encoding=result['encoding'])
                data_list = []  # List to hold each chunk
                for chunk in uploaded_data:
                    categorical_columns = chunk.select_dtypes(
                        include=['object', 'category']).columns
                    # st.write(categorical_columns)
                    data_list.append(chunk)  # Add chunk to list
                # Concatenate all chunks
                data = pd.concat(data_list, ignore_index=True)
            elif uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)

        except UnicodeDecodeError:
            st.error(
                "There was an error decoding the file. Please make sure the file is encoded in UTF-8 or try a different encoding.")

    return data


# def upload_and_read_large_file(key, instruction="Please upload a CSV or Excel file", type=["csv", "xlsx"]):

#     # Displaying the instruction message
#     # st.markdown(f"**{instruction}**")
#     uploaded_file = st.file_uploader(instruction, type=type, key=key)

#     data = None  # Placeholder for the DataFrame

#     if uploaded_file is not None:
#         # # Determine the file type and read the file into a Pandas DataFrame
#         try:
#             sample = uploaded_file.read(1000)  # Read the first 1000 bytes
#             result = chardet.detect(sample)
#             encoding = result['encoding']
#             uploaded_file.seek(0)
#             if uploaded_file.name.endswith('.csv'):
#                 uploaded_data = pd.read_csv(
#                     uploaded_file, chunksize=50000, encoding=encoding, encoding_errors='ignore')

#             elif uploaded_file.name.endswith('.xlsx'):
#                 data = pd.read_excel(uploaded_file)

#             data_list = []  # List to hold each chunk
#             for chunk in uploaded_data:
#                 data_list.append(chunk)  # Add chunk to list
#                 # Concatenate all chunks
#             data = pd.concat(data_list, ignore_index=True)
#         except UnicodeDecodeError:
#             st.error(
#                 "There was an error decoding the file. Please make sure the file is encoded in UTF-8 or try a different encoding.")

#     return data

def upload_and_read_large_file(key, instruction="Please upload a CSV or Excel file", type=["csv", "xlsx"]):
    uploaded_file = st.file_uploader(instruction, type=type, key=key)

    data = None  # Placeholder for the DataFrame

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                sample = uploaded_file.read(1000)  # Read the first 1000 bytes
                result = chardet.detect(sample)
                encoding = result['encoding']
                uploaded_file.seek(0)
                uploaded_data = pd.read_csv(
                    uploaded_file, chunksize=50000, encoding=encoding, encoding_errors='ignore')

                data_list = []  # List to hold each chunk
                for chunk in uploaded_data:
                    data_list.append(chunk)  # Add chunk to list
                data = pd.concat(data_list, ignore_index=True)

            elif uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)

        except UnicodeDecodeError:
            st.error(
                "There was an error decoding the file. Please make sure the file is encoded in UTF-8 or try a different encoding.")

    return data
