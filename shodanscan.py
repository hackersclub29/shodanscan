import subprocess
import time
import os

# Hardcoded Shodan API key
SHODAN_API_KEY = "provide your shodan api key here"

# Function to query Shodan for an IP
def query_shodan(ip):
    try:
        result = subprocess.check_output(["shodan", "host", ip], stderr=subprocess.STDOUT, text=True)
        print(f"Querying Shodan for {ip}")
        print(result)
        print("-" * 60)
        return True
    except subprocess.CalledProcessError as e:
        if "Error: No information available for that IP." in e.output:
            return False
        else:
            print(f"Error querying Shodan for {ip}")
            return False

# Check if the file exists and is not empty
if not os.path.isfile("file.lst") or os.path.getsize("file.lst") == 0:
    print("Error: IP list file 'file.lst' is either missing or empty.")
    exit(1)

# Set Shodan API key as an environment variable
os.environ["SHODAN_API_KEY"] = SHODAN_API_KEY

# Read each IP from the file and query Shodan with a 2-second gap
with open("file.lst", "r") as file:
    ip_list = file.read().splitlines()

for ip in ip_list:
    query_shodan(ip)
    time.sleep(1)  # Add a 1-second gap between scans

# Process the results if needed
# for ip, success in zip(ip_list, results):
#     if not success:
#         print(f"Failed to query Shodan for {ip}")
