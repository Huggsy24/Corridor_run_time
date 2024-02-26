import pandas as pd

# Read the Excel file and load the 'Travel times Outbound' sheet
df = pd.read_excel('2.xlsx', sheet_name='Travel times Outbound')

# Create a new DataFrame to store the modified data
output_df = pd.DataFrame(columns=df.columns)

# Variable to track whether 'Pattern' row has been encountered
pattern_row_encountered = False

# Iterate through the rows of the DataFrame
for index, row in df.iterrows():
    # Check if the cell in the first column contains 'Pattern:'
    if str(row.iloc[0]).startswith('Pattern:'):
        # Fill the cell below with 'Identified'
        output_df = pd.concat([output_df, row.to_frame().T], ignore_index=True)
        output_df.at[len(output_df), df.columns[1]] = 'Identified'
        pattern_row_encountered = True
    else:
        # Copy the current row to the output DataFrame, excluding empty rows
        if not all(row.isna()):
            output_df = pd.concat([output_df, row.to_frame().T], ignore_index=True)

# Export the modified DataFrame to a new Excel file
output_df.to_excel('modified_travel_times_outbound.xlsx', index=False)
