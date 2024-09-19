import re
import sys
import time
from datetime import datetime, timezone
import http.server
import socketserver
import threading

# Check if the jobid is passed as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 jobprog_webserver.py <jobid>")
    sys.exit(1)

# Get the jobid from the command-line argument
jobid = sys.argv[1]

# Specify your log file name
file_name = 'parselogs.lipsgcxap02.jobprog.log.out'

# HTML file to store job progress
html_file = 'job_progress.html'

# Function to check job status and write details to an HTML file
def check_job_status(jobid):
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

        # Prepare HTML content
        html_content = f"""
        <html>
        <head><title>Job Progress</title></head>
        <body>
        <h1>Job Progress for Job ID: {jobid}</h1>
        <p><strong>Job Start Time:</strong> {first_nowtm_dt}</p>
        <p><strong>Job End Time:</strong> {last_update_tm_dt}</p>
        <p><strong>Job Running Time:</strong> {running_time}</p>
        <p><strong>Total Data Processed:</strong> {data_output}</p>
        <p>Last update: {datetime.now(timezone.utc)}</p>
        </body>
        </html>
        """

        # Write HTML content to file
        with open(html_file, 'w') as f:
            f.write(html_content)

    else:
        html_content = f"""
        <html>
        <head><title>Job Progress</title></head>
        <body>
        <h1>No entries found for Job ID: {jobid}</h1>
        <p>Last check: {datetime.now(timezone.utc)}</p>
        </body>
        </html>
        """

        # Write HTML content to file
        with open(html_file, 'w') as f:
            f.write(html_content)

# Function to run the job check loop
def run_job_check_loop():
    try:
        while True:
            check_job_status(jobid)
            time.sleep(300)  # Wait for 5 minutes (300 seconds)
    except KeyboardInterrupt:
        print("\nExiting the job check loop. Goodbye!")

# Function to start the HTTP server
def start_server():
    PORT = 8000
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Start the web server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Run the job check loop in the main thread
run_job_check_loop()

