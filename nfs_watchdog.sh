#!/bin/bash
# Script authored by Brian Knight, Knight InfoTek
# This script monitors for stale NFS mounts and attempts to remount them if detected

# Define the log file where NFS watchdog activity will be logged
LOGFILE="/var/log/nfs_watchdog.log"

# Function to check for stale NFS mounts
check_stale_nfs() {
  # Loop through each mounted filesystem and filter out only NFS mounts
  mount | grep nfs | while read -r mountpoint
  do
    # Extract the mount point path (third field from the mount output)
    mnt=$(echo $mountpoint | awk '{print $3}')
    
    # Check if the mount point is accessible using the 'df' command
    # Redirect output to /dev/null and suppress errors
    if ! df "$mnt" > /dev/null 2>&1; then
      # If the mount is stale (not accessible), log the event with a timestamp
      echo "$(date): Stale NFS mount found at $mnt" >> "$LOGFILE"
      
      # Optionally attempt to remount the stale NFS mount
      echo "$(date): Attempting to remount $mnt" >> "$LOGFILE"
      
      # Force unmount the stale NFS mount and remount all NFS shares
      umount -f "$mnt" && mount -a
      
      # Check if the remount was successful
      if [ $? -eq 0 ]; then
        # Log a success message if remounting worked
        echo "$(date): Successfully remounted $mnt" >> "$LOGFILE"
      else
        # Log a failure message if remounting failed
        echo "$(date): Failed to remount $mnt" >> "$LOGFILE"
      fi
    fi
  done
}

# Main script execution
# Log the start of the NFS mount check with a timestamp
echo "$(date): Running NFS mount check" >> "$LOGFILE"

# Call the function to check for stale NFS mounts
check_stale_nfs
