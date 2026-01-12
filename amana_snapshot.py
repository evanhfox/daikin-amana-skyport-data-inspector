import requests
import json
import time
import getpass
from datetime import datetime

# ==========================================
# CONSTANTS & ENDPOINTS
# ==========================================
API_BASE = "https://api.daikinskyport.com"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def login():
    """Authenticates with Daikin Skyport and returns an access token."""
    print("\n--- Amana/Daikin Skyport Snapshot Tool ---")
    email = input("Enter Email: ")
    password = getpass.getpass("Enter Password: ") # Hides input for security
    
    print(f"\n[-] Attempting to log in as {email}...")
    url = f"{API_BASE}/users/auth/login"
    payload = {"email": email, "password": password}
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        print("[+] Login successful!")
        return data['accessToken']
    except requests.exceptions.RequestException as e:
        print(f"[!] Login failed: {e}")
        return None

def get_devices(token):
    """Retrieves the list of thermostats on the account."""
    url = f"{API_BASE}/devices"
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=auth_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to get devices: {e}")
        return []

def get_device_data(token, device_id):
    """Pulls the full data dump for a specific device."""
    url = f"{API_BASE}/deviceData/{device_id}"
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=auth_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to get device data: {e}")
        return {}

def clean_percent(val):
    """Converts Daikin's 0-200 scale to 0-100%."""
    try:
        return f"{float(val) / 2:.1f}%"
    except (ValueError, TypeError):
        return "N/A"

def save_raw_dump(device_name, data):
    """Saves the full JSON response to a file for deeper inspection."""
    # Clean filename (remove spaces/slashes)
    safe_name = "".join([c for c in device_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_DUMP_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[+] Full raw data saved to: {filename}")

def print_pretty_table(device_name, data):
    """Formats relevant data points into a readable table."""
    
    # Helper to check for multiple possible keys (e.g. Furnace vs Air Handler)
    def get_val(keys):
        if isinstance(keys, str): keys = [keys]
        for k in keys:
            if data.get(k) is not None:
                return data.get(k)
        return "N/A"

    metrics = [
        # Label, Key(s), Formatter
        ("Indoor Temp", "tempIndoor", lambda x: f"{x}°C"),
        ("Indoor Humidity", "humIndoor", lambda x: f"{x}%"),
        ("Outdoor Temp", "tempOutdoor", lambda x: f"{x}°C"),
        ("Outdoor Humidity", "humOutdoor", lambda x: f"{x}%"),
        ("-" * 20, None, None),
        ("System Status", "equipmentStatus", lambda x: {1:"Cool", 2:"Dehum", 3:"Heat", 4:"Fan", 5:"Idle"}.get(x, str(x))),
        ("Target Cool SP", "cspActive", lambda x: f"{x}°C"),
        ("Target Heat SP", "hspActive", lambda x: f"{x}°C"),
        ("Fan Mode", "fanCirculate", lambda x: {0:"Off", 1:"Always On", 2:"Schedule"}.get(x, str(x))),
        ("-" * 20, None, None),
        # Checks for Furnace (IFC) OR Air Handler (AH) keys
        ("Furnace Heat Demand", ["ctIFCHeatRequestedDemandPercent", "ctAHHeatRequestedDemandPercent"], clean_percent),
        ("AC Cool Demand", ["ctIFCCoolRequestedDemandPercent", "ctAHCoolRequestedDemandPercent"], clean_percent),
        ("Fan Demand", ["ctIFCFanRequestedDemandPercent", "ctAHFanRequestedDemandPercent"], clean_percent),
        ("Humidity Demand", ["ctIFCHumRequestedDemandPercent", "ctAHHumRequestedDemandPercent"], clean_percent),
    ]

    print("\n" + "="*45)
    print(f" DEVICE: {device_name}")
    print("="*45)
    print(f"{'METRIC':<25} | {'VALUE':<15}")
    print("-" * 45)
    
    for label, keys, formatter in metrics:
        if keys is None:
            print("-" * 45)
            continue
            
        raw_val = get_val(keys)
        
        if raw_val != "N/A" and formatter:
            val_str = formatter(raw_val)
        else:
            val_str = str(raw_
