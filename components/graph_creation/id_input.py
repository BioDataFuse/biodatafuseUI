import pandas as pd
from io import StringIO

def process_identifiers(uploaded_file, text_input) -> pd.DataFrame:
    """convert the input identifier list to a dataframe.

    @param uploaded_file: a CSV or TXT file contains identifiers
    @param text_input: the identifiers in the st.text_area (one identifier per line)

    :returns: a DataFrame containing the list of identifiers
    """
    identifiers_df = pd.DataFrame()  # Initialize an empty DataFrame
    warnings = []  # Initialize empty list for warnings

    # Process identifiers from text input
    if text_input.strip():
        identifiers_from_text = text_input.strip().split('\n')
        identifiers_df['Identifier'] = identifiers_from_text

    # Process identifiers from uploaded file
    if uploaded_file:
        # Ensure file type is CSV or TXT
        if uploaded_file.filename.endswith(('.csv', '.txt')):
            # Read the uploaded file
            file_contents = uploaded_file.read().decode("utf-8")
            identifiers_from_file = pd.read_csv(StringIO(file_contents), header=None, squeeze=True)
            
            # Append identifiers from file to DataFrame
            identifiers_df = pd.concat([identifiers_df, identifiers_from_file])
        else:
            warnings.append("Unsupported file format. Please upload a CSV or TXT file.")

    # Check if neither uploaded file nor text input provided
    if identifiers_df.empty and not warnings:
        warnings.append("Please provide your identifiers!")

    return identifiers_df, warnings
