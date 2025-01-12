import pandas as pd
from pathlib import Path
import os

def combine_csv_files():
    # Get the current directory where the script is located
    base_path = Path(os.getcwd())

    # List to store all dataframes
    all_dfs = []

    # Counter for progress tracking
    total_files = 0
    processed_files = 0

    # First count total CSV files
    for csv_file in base_path.rglob('*.csv'):
        total_files += 1

    # Process each CSV file
    for csv_file in base_path.rglob('*.csv'):
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)

            # Add a column for the conversation source (using the parent folder name)
            df['conversation_id'] = csv_file.parent.name

            # Append to our list of dataframes
            all_dfs.append(df)

            # Update progress
            processed_files += 1
            if processed_files % 100 == 0:
                print(f"Processed {processed_files}/{total_files} files...")

        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")

    # Combine all dataframes
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Save the combined dataframe
        output_path = base_path / 'combined_messages.csv'
        combined_df.to_csv(output_path, index=False)
        print(f"\nSuccessfully combined {len(all_dfs)} files into {output_path}")
        print(f"Total rows in combined file: {len(combined_df)}")
    else:
        print("No CSV files were found or processed successfully.")

if __name__ == "__main__":
    combine_csv_files()
