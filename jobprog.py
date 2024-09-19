import re
import sys
from datetime import datetime, timezone

# Check if the jobid is passed as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 jobprog.py <jobid>")
    sys.exit(1)

# Get the jobid from the command-line argument
jobid = sys.argv[1]

# Specify your file name
file_name = 'parselogs.lipsgcxap02.jobprog.log.out'

# Read the file content
with open(file_name, 'r') as file:
    file_content = file.read()

# Regular expression to find entries matching the jobid, nowtm, update_tm, and sofar_bytes
job_pattern = re.compile(rf'"jobid": {jobid},.*?"nowtm": (\d+).*?"update_tm": (\d+).*?"sofar_bytes": (\d+)', re.DOTALL)

# Find all matches for the given jobid
matches = job_pattern.findall(file_content)

if matches:
    # Get the first nowtm, last update_tm, and last sofar_bytes for the job
    first_nowtm = matches[0][0]
    last_update_tm = matches[-1][1]
    last_sofar_bytes = matches[-1][2]

    # Convert epoch timestamps to human-readable format (UTC timezone-aware)
    first_nowtm_dt = datetime.fromtimestamp(int(first_nowtm), timezone.utc)
    last_update_tm_dt = datetime.fromtimestamp(int(last_update_tm), timezone.utc)

    # Calculate the running time of the job
    running_time = last_update_tm_dt - first_nowtm_dt

    # Convert the last sofar_bytes to megabytes (MB) or terabytes (TB)
    last_sofar_bytes_value = int(last_sofar_bytes)
    if last_sofar_bytes_value >= 1024 ** 4:
        # Display in TB if value is large enough
        last_sofar_tb = last_sofar_bytes_value / (1024 ** 4)
        data_output = f"{last_sofar_tb:.2f} TB"
    else:
        # Display in MB by default
        last_sofar_mb = last_sofar_bytes_value / (1024 ** 2)
        data_output = f"{last_sofar_mb:.2f} MB"

    # Output the jobid, times, and data processed
    print(f"Job ID: {jobid}")
    print(f"Job Start Time: {first_nowtm_dt}")
    print(f"Job End Time: {last_update_tm_dt}")
    print(f"Job Running Time: {running_time}")
    print(f"Total Data Processed: {data_output}")

else:
    print(f"No entries found for jobid: {jobid}")

