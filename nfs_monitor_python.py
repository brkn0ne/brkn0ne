import time
from datetime import datetime

# Function to read and parse NFS statistics from /proc/self/mountstats
def parse_nfs_stats():
    nfs_stats = {}
    
    # Open the file where mount statistics are stored
    with open('/proc/self/mountstats', 'r') as file:
        lines = file.readlines()

    # Loop through lines to find NFS-specific stats
    for line in lines:
        if 'nfs' in line:
            # Extract NFS version and mount details
            mount_details = line.strip().split()
            nfs_stats['mount'] = mount_details[4]
            nfs_stats['nfs_version'] = mount_details[3]

        # Look for NFS read/write performance data
        if line.startswith(' per-op statistics'):
            # Extract performance stats
            stats_line = next(file).strip().split()
            nfs_stats['read_ops'] = stats_line[1]
            nfs_stats['write_ops'] = stats_line[3]
            nfs_stats['read_bytes'] = stats_line[5]
            nfs_stats['write_bytes'] = stats_line[7]
            nfs_stats['read_time'] = stats_line[9]
            nfs_stats['write_time'] = stats_line[11]

    return nfs_stats

# Function to monitor NFS stats and print results
def monitor_nfs():
    try:
        while True:
            # Get the current NFS stats
            nfs_stats = parse_nfs_stats()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Print the collected stats
            print(f"\n--- NFS Performance at {timestamp} ---")
            print(f"Mount: {nfs_stats.get('mount', 'N/A')}")
            print(f"NFS Version: {nfs_stats.get('nfs_version', 'N/A')}")
            print(f"Read Ops: {nfs_stats.get('read_ops', '0')}")
            print(f"Write Ops: {nfs_stats.get('write_ops', '0')}")
            print(f"Read Bytes: {nfs_stats.get('read_bytes', '0')} bytes")
            print(f"Write Bytes: {nfs_stats.get('write_bytes', '0')} bytes")
            print(f"Read Time: {nfs_stats.get('read_time', '0')} ms")
            print(f"Write Time: {nfs_stats.get('write_time', '0')} ms")

            # Sleep for 5 minutes before running again
            time.sleep(300)
    except KeyboardInterrupt:
        print("\nStopping NFS monitor.")

# Run the NFS monitor
monitor_nfs()

