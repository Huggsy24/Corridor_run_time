import pandas as pd

def finalize_with_appended_custom_time_header(excel_file_path):
    # Load the Excel file
    df = pd.read_excel(excel_file_path)
    
    # Extract and sort unique "Start Time" values, ignoring NaNs
    start_time_values = df['Start Time'].dropna().unique()
    sorted_start_times = sorted(start_time_values)
    
    # Convert time values to four-digit strings (HHMM format), then append "3559" as the final header
    time_headers = [f'{int(time):04d}' for time in sorted_start_times] + ['3559']
    
    # Filter rows explicitly for stop ID values, ignoring "Stop ID:" rows and NaNs
    stop_id_rows = df[df['Unnamed: 0'].str.contains('Stop ID:', na=False) & (df['Unnamed: 1'] != 'Stop ID:')]
    
    # Initialize a list to keep track of unique stop ID combinations
    unique_stop_id_combinations = []
    
    # Iterate over each row in the filtered dataframe to extract and store unique combinations
    for _, row in stop_id_rows.iterrows():
        stop_ids = row[df.columns[1:]].dropna().values  # Extract stop IDs, ignoring NaN values
        # Generate combinations as tuples (start stop, end stop) and add to the list if not already present
        for start_stop, end_stop in zip(stop_ids[:-1], stop_ids[1:]):  # Exclude the last stop as it has no next stop
            if start_stop != "Stop ID:" and end_stop != "Stop ID:":
                combination = (start_stop, end_stop)
                if combination not in unique_stop_id_combinations:
                    unique_stop_id_combinations.append(combination)
    
    # Convert the list of tuples into a dataframe, with Start and End Stop IDs in the first two columns
    unique_combinations_df = pd.DataFrame(unique_stop_id_combinations, columns=['Start Stop ID', 'End Stop ID'])
    
    # Exclude any rows where 'Start Stop ID' or 'End Stop ID' contains 'Stop ID:'
    filtered_combinations_df = unique_combinations_df[~unique_combinations_df['Start Stop ID'].astype(str).str.contains('Stop ID:') & 
                                                      ~unique_combinations_df['End Stop ID'].astype(str).str.contains('Stop ID:')]
    
    # Create column headers including "Start Stop ID", "End Stop ID", followed by the clean time headers
    column_headers = ['Start Stop ID', 'End Stop ID'] + time_headers
    
    # Construct the final DataFrame with correct headers
    final_df = pd.DataFrame(columns=column_headers)
    final_df = pd.concat([final_df, filtered_combinations_df], ignore_index=True)
    
    return final_df

# Example usage
excel_file_path = 'Lu___Ve_Vacances_ete_et_Noël_service_block.xlsx'  # Replace with your file path
final_df = finalize_with_appended_custom_time_header(excel_file_path)
output_file_path = 'Timing_Grid.xlsx'  # Replace with your desired output file name
final_df.to_excel(output_file_path, index=False)
