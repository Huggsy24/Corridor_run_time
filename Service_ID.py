import pandas as pd

# Function to group blocks of data by service ID
def group_service_blocks_by_id(df):
    grouped_blocks = {}
    current_service_id = None
    for i, row in df.iterrows():
        # Check for 'Service ID:' label
        if row['Unnamed: 0'] == 'Service ID:':
            current_service_id = row['Unnamed: 1']
            if current_service_id not in grouped_blocks:
                grouped_blocks[current_service_id] = []
        # Identify the start of a new block within the same service ID
        elif pd.notnull(row['Unnamed: 0']) and current_service_id:
            if 'start_index' not in locals() or start_index < i - 1:
                start_index = i
            end_index = i
            # Add the block to the current service ID
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

# Group the service blocks in the dataframe
grouped_service_blocks_by_id = group_service_blocks_by_id(data_df)

# Save the grouped blocks to Excel files, one per service ID
saved_files = save_grouped_blocks_to_excel(grouped_service_blocks_by_id, data_df)

# The saved_files variable contains the paths to the saved Excel files
