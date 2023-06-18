#!/bin/bash
###################################################################################
#
# Script Name 	- split_file.sh
# Args		- <input_file> <Split Size>
# Description	- Splits Large files into smaller chunks for Backup
# Date		- June 16 2023
# Auther 	- Brian Knight
# Contact 	- Brian@KnightInfoTek.com
#
####################################################################################

# Usage statement
usage() {
    echo "Usage: $0 <input_file> <chunk_size>"
    echo "Example: $0 large_file 100M"
    exit 1
}

# Check the number of arguments
if [ "$#" -ne 2 ]; then
    usage
fi

# Store the input file and chunk size from command-line arguments
input_file="$1"
chunk_size="$2"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' does not exist."
    usage
fi

# Split the file into smaller parts
split --bytes="$chunk_size" "$input_file" "$input_file.part"

# Calculate the hash of the original file
original_hash=$(md5sum "$input_file" | awk '{print $1}')

# Create a metadata file for reconstruction map
metadata_file="$input_file.metadata"
echo "Original File: $input_file" > "$metadata_file"
echo "Chunk Size: $chunk_size" >> "$metadata_file"
echo "Original Hash: $original_hash" >> "$metadata_file"
echo "File Parts:" >> "$metadata_file"
for part in "$input_file".part*; do
    echo "- $part" >> "$metadata_file"
done

# Save the hash to a file for Auth
echo "$original_hash" > "$input_file.hash"

# Display completion message
echo "File split completed."
echo "Metadata File: $metadata_file"
