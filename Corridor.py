import pandas as pd

# Assuming the file is named 'modified_travel_times_outbound_corrected.xlsx' and is in the same directory
file_name = 'modified_travel_times_outbound_corrected.xlsx'

# Read the entire sheet into a DataFrame
data = pd.read_excel(file_name, sheet_name='Sheet1', header=None)

# Function to extract Service ID from a cell (assuming the format is "Service ID: XXX")
def extract_service_id(cell_value):
    if pd.isnull(cell_value):
        return None
    if "Service ID:" in cell_value:
        return cell_value.split(":")[1].strip()
    return None

# Iterate over the DataFrame to group rows by Service ID
groups = {}
current_service_id = None
for index, row in data.iterrows():
    service_id = extract_service_id(row[0])
    if service_id:
        current_service_id = service_id
        if current_service_id not in groups:
            groups[current_service_id] = []
    if current_service_id:
        groups[current_service_id].append(row)

# Convert lists of rows back into DataFrames
for service_id, rows in groups.items():
    groups[service_id] = pd.DataFrame(rows).reset_index(drop=True)

# Now you have a dictionary `groups` with Service ID as keys and DataFrames as values

# Example: Saving each group to a separate Excel file
for service_id, df in groups.items():
    output_file = f'service_id_{service_id}.xlsx'  # Naming the output files
    # Clean the DataFrame if necessary (e.g., remove NaNs)
    df_cleaned = df.dropna(how='all').reset_index(drop=True)
    # Save to Excel
    df_cleaned.to_excel(output_file, index=False)

# Step 3: Apply the transformation (simplified version based on the example)
for index, row in data.iterrows():
    if '-' in str(row[0]):  # Adjust the index 0 if your time values are in a different column
        start_time, end_time = row[0].split('-')
        data.at[index, 'Start Time'] = start_time
        data.at[index, 'End Time'] = end_time
        data.at[index, 0] = None  # Set the original column value to None
        data.at[index, 1] = None  # Set the original column value to None

# Reorder columns to have Start Time and End Time at the front
data = data[['Start Time', 'End Time', 0] + [col for col in data.columns if col not in ['Start Time', 'End Time', 0]]]

# Step 4: Export the modified DataFrame to Excel
modified_output_file = 'service_ids_isolated.xlsx'
data.to_excel(modified_output_file, index=False)
print(f"Modified data exported to {modified_output_file}")

# Step 5: Review the results
print(data.head(10))
