# Amana/Daikin Skyport Data Snapshot

A standalone Python script to query Amana Smart Thermostats (and Daikin One+) for detailed system performance data.

## ⚠️ Important: Scope of this Tool
**This script is designed for "Point-in-Time" diagnostics only.**

It performs a single "grab" of the current data from the cloud API to help you see what your system is doing *right now*. It does **not** run continuously, it does not record history, and it does not generate graphs.

### Looking for historical graphs & trending?
If you want to track humidity demand over time, plot furnace runtime, or visualize data history, this script is not enough. You need a system that polls the API 24/7 and stores the data in a database. This data would then need to be visualized in something like Grafana.

* **For Home Assistant Users:**
    I highly recommend using the full integration which handles polling, entities, and history automatically:
    [Daikin Skyport Integration for Home Assistant](https://github.com/apetrycki/daikinskyport)

* **For Custom Solutions:**
    To achieve historical logging without Home Assistant, you would need to substantially rework this script into a continuously running application (e.g., a service that loops every 60 seconds and writes to InfluxDB, SQL, or CSV).

---

## What this tool does

1.  **Live Table View:** Connects to the Skyport cloud API and prints a clean, readable table of your system's *current* status (Humidity Demand, Fan Demand, Temperatures, etc.).
2.  **Full Data Dump (The "Black Box"):** Automatically saves a `.json` file containing the **entire** raw data set returned by the thermostat.

## Why is the Data Dump useful?

The API returns over 900 data points. The on-screen table only shows the most common ones. By looking at the generated JSON file, you can see **everything** your system knows, including:
* **Equipment-Specific Data:** Differences between Furnaces (`ctIFC...`) and Air Handlers (`ctAH...`).
* **Fault Codes:** History of error codes and alerts.
* **Configuration:** Detailed settings for staging, ramp profiles, and timers.

## Prerequisites
* **Python 3.x** installed on your computer.
* No external libraries are required (uses standard `json`, `requests`, etc. included with Python).

## How to Use

1.  **Download the script:**
    Download `amana_snapshot.py` to your computer.

2.  **Run the script:**
    Open your terminal or command prompt and run:
    ```bash
    python amana_snapshot.py
    ```

3.  **Enter Credentials:**
    The script will prompt you for your **email** and **password**.
    * *Note: These are the same credentials you use for the Amana/Daikin mobile app.*

4.  **View Output:**
    * **Terminal:** You will see the summarized table immediately.
    * **File:** Look in the same folder for a file named something like `MainFloor_DUMP_20260112.json`. Open this with any text editor to see the full raw data.

## Understanding the Data
The data points you see will depend on your specific installation:

* **Prefix `ctIFC`**: Stands for **Indoor Furnace Control** (Gas Furnace data usually lives here).
* **Prefix `ctAH`**: Stands for **Air Handler** (Heat Pump/Electric Air Handler data usually lives here).
* **Values**: The API returns demand values on a **0-200 scale**. This script automatically converts them to standard percentages (0-100%) for readability in the table.

## Disclaimer
This is an unofficial tool. It uses the same API endpoints as the mobile app but is not supported or endorsed by Daikin or Amana. Use at your own risk.
