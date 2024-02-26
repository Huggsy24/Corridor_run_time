import pandas as pd

# Read the Excel file
df = pd.read_excel('2.xlsx', sheet_name='Route Outbound')

# Initialize an empty list to store the sections
sections = []

# Iterate through the values in the first column
for index, value in enumerate(df.iloc[:, 0]):
    if value == "Stop Number":
        # Get the values in the row whenever "Stop Number" is encountered, excluding blank cells
        stop_number_row = df.iloc[index, :].tolist()
        stop_number_row_without_blanks = [cell for cell in stop_number_row if pd.notna(cell)]
        sections.append(stop_number_row_without_blanks)
    elif value not in ["Timing Point Code", "Stop Name", "Distance", "Factor", ""]:
        sections.append([value])

# Create a DataFrame with the filtered sections
result_df = pd.DataFrame(sections)

# Export the DataFrame to a new Excel file
result_df.to_excel('filtered_sections.xlsx', index=False, header=False)
