import pandas as pd
from pyBiodatafuse.data_loader import create_df_from_text

def process_identifiers(uploaded_file, text_input) -> pd.DataFrame:
    """convert the input identifier list to a dataframe.

    @param uploaded_file: a CSV or TXT file contains identifiers
    @param text_input: the identifiers in the st.text_area (one identifier per line)

    :returns: a DataFrame containing the list of identifiers
    """
    identifiers_df = pd.DataFrame()  # Initialize an empty DataFrame
    warnings = []  # Initialize empty list for warnings

    # Process identifiers from text input
    if text_input:
        # Create a DataFrame from the list of identifiers
        identifiers_df = create_df_from_text(text_input)

    # Process identifiers from uploaded file
    if uploaded_file:
        # Read the uploaded file
        file_contents = uploaded_file.getvalue().decode("utf-8")
        identifiers_df = pd.concat([identifiers_df, create_df_from_text(file_contents)], ignore_index=True).drop_duplicates()
        
    # Check if neither uploaded file nor text input provided
    if identifiers_df.empty and not warnings:
        warnings.append("Please provide your identifier(s)!")

    return identifiers_df.to_dict('records'), warnings
