import pandas as pd

# Load the Excel file
df_route_outbound = pd.read_excel('2.xlsx', sheet_name='Route Outbound')
df_travel_times_outbound = pd.read_excel('2.xlsx', sheet_name='Travel times Outbound')

# Stage One: Capture Sections and Populate pattern_stops
sections = []
pattern_stops = {}
current_pattern = None
for index, row in df_route_outbound.iterrows():
    value = row.iloc[0]
    if pd.notna(value) and value not in ["Stop Number", "Timing Point Code", "Stop Name", "Distance", "Factor", ""]:
        current_pattern = value  # Capture the pattern identifier
        sections.append([current_pattern])  # Initialize section with pattern identifier
        pattern_stops[current_pattern] = []  # Initialize dictionary entry for current pattern
    elif value == "Stop Number" and current_pattern:
        stop_numbers = [cell for cell in row[1:] if pd.notna(cell)]  # Extract non-null stop numbers
        sections[-1].extend(stop_numbers)  # Append stop numbers to the current pattern's section
        pattern_stops[current_pattern].extend(stop_numbers)  # Update pattern_stops dictionary

# Process 'Travel times Outbound' sheet and update with stop numbers
for index, row in df_travel_times_outbound.iterrows():
    if str(row.iloc[0]).startswith('Pattern:'):
        pattern_key = row.iloc[1]
        if pattern_key in pattern_stops:
            stop_numbers = pattern_stops[pattern_key]
            required_columns = len(stop_numbers) + 1
            current_columns = len(df_travel_times_outbound.columns)
            if required_columns > current_columns:
                additional_cols = required_columns - current_columns
                for i in range(additional_cols):
                    df_travel_times_outbound[f'Unnamed: {current_columns + i}'] = None
            # Insert "Stop ID:" in the cell underneath "Pattern:"
            pattern_index = row.name
            df_travel_times_outbound.at[pattern_index + 1, df_travel_times_outbound.columns[0]] = "Stop ID:"
            for stop_index, stop_number in enumerate(stop_numbers, start=1):
                df_travel_times_outbound.at[index + 1, df_travel_times_outbound.columns[stop_index]] = stop_number

# Export the modified 'Travel times Outbound' DataFrame
df_travel_times_outbound.to_excel('modified_travel_times_outbound_corrected.xlsx', index=False)

# Convert sections to DataFrame for export
sections_df = pd.DataFrame(sections, columns=['Pattern'] + list(range(1, len(sections[0]))))

# Seperate each Service IDs

# Split Start times and End times into seperate columns

# Loop through all the different combination of stops, list running times between stops based on start time. 

# Build back patterns so that the combination above are listed for each stop. If the start time and end time of one stop 
# covers the entire period of a number, duplicate so that you have even splits across all stop patterns. 

# For each pattern, if the timeband above it is equal to the one below, merge them so you take the start time from the 
# first row and end time from the second row. 

# Merge back the start and end times to match input format

# Loop through service IDs
