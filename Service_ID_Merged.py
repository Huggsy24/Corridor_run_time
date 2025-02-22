import pandas as pd

# Function to group blocks of data by service ID
def group_service_blocks_by_id(df):
    grouped_blocks = {}
    current_service_id = None
    start_index = None  # Initialize start_index outside of the loop
    
    for i, row in df.iterrows():
        if row['Unnamed: 0'] == 'Service ID:':
            current_service_id = row['Unnamed: 1']
            if current_service_id not in grouped_blocks:
                grouped_blocks[current_service_id] = []
            start_index = None  # Reset start_index whenever a new service ID is encountered

        elif pd.notnull(row['Unnamed: 0']) and current_service_id:
            if start_index is None:  # A new block starts when start_index is None
                start_index = i
            end_index = i
            
            # Check if we have reached the end of a block
            if i < len(df) - 1 and pd.isnull(df.iloc[i + 1]['Unnamed: 0']):
                # Add the block to the current service ID and reset start_index
                grouped_blocks[current_service_id].append({'start_index': start_index, 'end_index': end_index})
                start_index = None  # Important to reset start_index for the next block

    # Make sure to add the last block if the DataFrame ends with a block
    if start_index is not None:
        grouped_blocks[current_service_id].append({'start_index': start_index, 'end_index': end_index})

    return grouped_blocks

# Function to save grouped blocks to Excel, one file per service ID
def save_grouped_blocks_to_excel(grouped_blocks, df):
    file_paths = []
    for service_id, blocks in grouped_blocks.items():
        combined_df = pd.DataFrame()
        for block in blocks:
            block_df = df.iloc[block['start_index']:block['end_index'] + 1]
            combined_df = pd.concat([combined_df, block_df], ignore_index=True)
        # Create a file-safe service ID
        service_id_safe = service_id.replace(" ", "_").replace("-", "_").replace("/", "_").replace(",", "").replace("é", "e")
        file_name = f"{service_id_safe}_service_block.xlsx"
        file_path = f"/Users/hugo.cooke/dev/Scripts_Work/Corridor_running_times/{file_name}"  # Update this path as needed
        combined_df.to_excel(file_path, index=False)
        file_paths.append(file_path)
    return file_paths

# Specify the file name
file_name = 'modified_travel_times_outbound_corrected.xlsx'

# Read the provided Excel file into a DataFrame
data_df = pd.read_excel(f'/Users/hugo.cooke/dev/Scripts_Work/Corridor_running_times/{file_name}')  # Update the path as needed

# Apply the transformation to separate "XXXX-XXXX" time values
for index, row in data_df.iterrows():
    if '-' in str(row[0]):  # This checks for the "XXXX-XXXX" format
        start_time, end_time = row[0].split('-')
        data_df.at[index, 'Start Time'] = start_time.strip()
        data_df.at[index, 'End Time'] = end_time.strip()
        data_df.at[index, 0] = None  # Nullify only the "XXXX-XXXX" entries, not deleting the column
    # Additional transformations or checks can be performed here if needed

# Ensure that during the final steps, when we reorder or clean up columns, we retain all necessary data:
data_df = data_df[['Start Time', 'End Time'] + [col for col in data_df.columns if col not in ['Start Time', 'End Time', 0]]]

# Reorder columns to have Start Time and End Time at the front, if not already
data_df = data_df[['Start Time', 'End Time'] + [col for col in data_df.columns if col not in ['Start Time', 'End Time']]]

# Group the service blocks in the dataframe
grouped_service_blocks_by_id = group_service_blocks_by_id(data_df)

# Save the grouped blocks to Excel files, one per service ID
saved_files = save_grouped_blocks_to_excel(grouped_service_blocks_by_id, data_df)