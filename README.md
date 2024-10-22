# Finding Duplicate Mac Addresses 

This Python script is used to gather data about duplicate mac addresses across different clusters.
Developed by Rushabh Jain (rushabh.jain@nutanix.com)

## Features

- Fetches all vms amd their network name, mac addresses for given clusters


## Requirements

- Python 3.8 >= 
- PC Ips in pc.csv file
- Cluster Credentials for PC (must be same or use a service account)

## Setup

1. Download the script files on your system along with the requirements.

2. Create a virtual environment (optional but recommended):

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages (if required) :

    ```bash
    pip3 install -r requirements.txt
    ```

## Usage



1. Run the script:

    ```
    python3 mac_addresses.py
    ```


2. The script will fetch the results in output files.
