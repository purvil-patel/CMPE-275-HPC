import pandas as pd

csv_files_directory = '../data/'

# Load the CSV files
df1 = pd.read_csv(f'{csv_files_directory}records_per_second_process_0.csv')
df2 = pd.read_csv(f'{csv_files_directory}records_per_second_process_1.csv')
df3 = pd.read_csv(f'{csv_files_directory}records_per_second_process_2.csv')

# Merge the dataframes on the 'Seconds' column
merged_df = df1.merge(df2, on='Seconds', how='outer', suffixes=('-P0', '-P1'))
merged_df = merged_df.merge(df3, on='Seconds', how='outer')

# Rename columns appropriately
merged_df.columns = ['Seconds', 'RecordsProcessed-P0', 'RecordsProcessed-P1', 'RecordsProcessed-P2']

# Fill missing values with 0, assuming missing values should be treated as 0
merged_df.fillna(0, inplace=True)

# Sort the dataframe based on 'Seconds' column
merged_df.sort_values(by='Seconds', inplace=True)

# Reset index after sorting
merged_df.reset_index(drop=True, inplace=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('../final_data/merged_file.csv', index=False)

print("Merging complete. The merged data is saved as 'merged_file.csv'.")
