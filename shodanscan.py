import subprocess
import time
import os
import requests

# Hardcoded Shodan API key
SHODAN_API_KEY = "provide here shodan API key"
# IPinfo API key (replace 'YOUR_IPINFO_API_KEY' with your actual API key)
IPINFO_API_KEY = "Provide here ipinfo token"

# Function to query Shodan for an IP
def query_shodan(ip):
    try:
        result = subprocess.check_output(["shodan", "host", ip], stderr=subprocess.STDOUT, text=True)
        print(f"Querying Shodan for {ip}")
        print(result)
        print("-" * 60)  # Add a separation line with a new line
        return True
    except subprocess.CalledProcessError as e:
        if "Error: No information available for that IP." in e.output:
            return False
        else:
            print(f"Error querying Shodan for {ip}")
            return False

# Function to query IPinfo for additional information
def query_ipinfo(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json?token={IPINFO_API_KEY}"
        response = requests.get(url)
        ip_info = response.json()

        print(f"Querying IPinfo for {ip}")
        print(f"IP: {ip}")
        print(f"City: {ip_info.get('city', 'Na')}")
        print(f"Region: {ip_info.get('region', 'Na')}")
        print(f"Country: {ip_info.get('country', 'Na')}")
        print(f"Location: {ip_info.get('loc', 'Na')}")
        print(f"Timezone: {ip_info.get('timezone', 'Na')}")

        asn_info = ip_info.get('asn', {})
        print(f"ASN: {asn_info.get('asn', 'Na')}")
        print(f"ASN Name: {asn_info.get('name', 'Na')}")
        print(f"ASN Domain: {asn_info.get('domain', 'Na')}")
        print(f"ASN Route: {asn_info.get('route', 'Na')}")
        print(f"ASN Type: {asn_info.get('type', 'Na')}")

        company_info = ip_info.get('company', {})
        print(f"Company Name: {company_info.get('name', 'Na')}")
        print(f"Company Domain: {company_info.get('domain', 'Na')}")
        print(f"Company Type: {company_info.get('type', 'Na')}")

        privacy_info = ip_info.get('privacy', {})
        print(f"VPN: {privacy_info.get('vpn', 'Na')}")
        print(f"Proxy: {privacy_info.get('proxy', 'Na')}")
        print(f"Tor: {privacy_info.get('tor', 'Na')}")
        print(f"Relay: {privacy_info.get('relay', 'Na')}")
        print(f"Hosting: {privacy_info.get('hosting', 'Na')}")
        print(f"Service: {privacy_info.get('service', 'Na')}")

        abuse_info = ip_info.get('abuse', {})
        print(f"Abuse Address: {abuse_info.get('address', 'Na')}")
        print(f"Abuse Country: {abuse_info.get('country', 'Na')}")
        print(f"Abuse Email: {abuse_info.get('email', 'Na')}")
        print(f"Abuse Name: {abuse_info.get('name', 'Na')}")
        print(f"Abuse Network: {abuse_info.get('network', 'Na')}")
        print(f"Abuse Phone: {abuse_info.get('phone', 'Na')}")

        domains_info = ip_info.get('domains', {})
        print(f"Total Domains: {domains_info.get('total', 'Na')}")
        print(f"Domain List: {domains_info.get('domains', 'Na')}")

        print("-" * 60)  # Add a separation line with a new line
        return True
    except Exception as e:
        print(f"Error querying IPinfo for {ip}: {e}")
        return False

# Check if the file exists and is not empty
if not os.path.isfile("file.lst") or os.path.getsize("file.lst") == 0:
    print("Error: IP list file 'file.lst' is either missing or empty.")
    exit(1)

# Set Shodan API key as an environment variable
os.environ["SHODAN_API_KEY"] = SHODAN_API_KEY

# Read each IP from the file and query Shodan and IPinfo with a 2-second gap
with open("file.lst", "r") as file:
    ip_list = file.read().splitlines()

try:
    for ip in ip_list:
        query_shodan(ip)
        time.sleep(2)  # Add a 2-second gap between Shodan scans
        query_ipinfo(ip)
        time.sleep(2)  # Add a 2-second gap between IPinfo scans

except KeyboardInterrupt:
    print("\nScript interrupted by user. Exiting...")
    exit(0)
