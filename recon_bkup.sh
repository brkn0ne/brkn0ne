#!/bin/bash
###################################################################################
#
# Script Name 	- recon_bkup.sh
# Args		- <metadata_file> from split_file.sh
# Description	- Reconstruct files after Restore 
# Date		- June 16 2023
# Auther 	- Brian Knight
# Contact 	- Brian@KnightInfoTek.com
#
####################################################################################
# Usage statement
usage() {
    echo "Usage: $0 <metadata_file>"
    echo "Example: $0 large_file.metadata"
    exit 1
}

# Check the number of arguments
if [ "$#" -ne 1 ]; then
    usage
fi

# Store the metadata file from the command-line argument
metadata_file="$1"


# Check if the metadata file exists
if [ ! -f "$metadata_file" ]; then
    echo "Error: Metadata file '$metadata_file' does not exist."
    usage
fi



# Read the metadata file and extract information
original_file=$(grep "Original File:" "$metadata_file" | cut -d " " -f 3-)
chunk_size=$(grep "Chunk Size:" "$metadata_file" | cut -d " " -f 3-)
original_hash=$(grep "Original Hash:" "$metadata_file" | cut -d " " -f 3-)
file_parts=$(grep "File Parts:" -A999 "$metadata_file" | grep -v "File Parts:" | awk '{print $2}')

# Reconstruct the file
reconstructed_file="${original_file%.*}_reconstructed.${original_file##*.}"

# Loop through the file parts and append them to the reconstructed file
for part in $file_parts; do
    cat "$part" >> "$reconstructed_file"
done


# Calculate the hash of the reconstructed file
reconstructed_hash=$(md5sum "$reconstructed_file" | awk '{print $1}')

# Compare the original and reconstructed hashes
if [ "$original_hash" == "$reconstructed_hash" ]; then
    echo "File reconstruction completed successfully."
    echo "Reconstructed file: $reconstructed_file"
    echo "Reconstructed file hash: $reconstructed_hash"
    echo "matches $original_hash"
else
    echo "Error: File reconstruction failed. The reconstructed file may be corrupted."
fi
