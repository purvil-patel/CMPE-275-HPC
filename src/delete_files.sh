#!/bin/bash

# The directory to delete files from, provided as the first script argument
DIRECTORY=$1

# Check if directory path is provided
if [ -z "$DIRECTORY" ]; then
  echo "Usage: $0 <directory_path>"
  exit 1
fi

# Check if the provided directory exists
if [ ! -d "$DIRECTORY" ]; then
  echo "Directory does not exist: $DIRECTORY"
  exit 1
fi

# Array of filenames to delete
declare -a files=("cleaned_data_rank_0.csv"
                  "cleaned_data_rank_1.csv"
                  "cleaned_data_rank_2.csv"
                  "log_process_0.txt"
                  "log_process_1.txt"
                  "log_process_2.txt"
                  "combined_cleaned_data.csv")

# Loop through the array and delete each file
for file in "${files[@]}"; do
  filepath="$DIRECTORY/$file"
  if [ -f "$filepath" ]; then
    rm "$filepath"
    echo "Deleted $filepath"
  else
    echo "File does not exist: $filepath"
  fi
done
