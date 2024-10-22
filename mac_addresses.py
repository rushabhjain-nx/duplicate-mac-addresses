import requests
import csv
import json
import urllib3
from collections import defaultdict
from typing import List, Dict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def find_duplicate_macs(data: List[List[str]]) -> Dict[str, List[str]]:
    
    mac_to_vms = defaultdict(list)
    
   
    for index, entry in enumerate(data):
        if len(entry) == 4:
            cluster_name, vm_name, network_name, mac_address = entry
            mac_to_vms[mac_address].append(vm_name)
        else:
            print(f"Skipping invalid entry at index {index}: {entry}")

    
    duplicates = {mac: vms for mac, vms in mac_to_vms.items() if len(vms) > 1}
    
    return duplicates

def print_duplicates(duplicates: Dict[str, List[str]]):

    if duplicates:
        print("\t Duplicate MAC Addresses:")
        for mac, vms in duplicates.items():
            print(f"\t ==> MAC Address: {mac} is associated with VMs: {', '.join(vms)}")
            #print()
    else:
        print("\t No duplicate MAC addresses found.")

def write_duplicates_to_csv(duplicates: Dict[str, List[str]], output_file: str):
   
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['MAC Address', 'VM Names']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for mac, vms in duplicates.items():
            writer.writerow({'MAC Address': mac, 'VM Names': ', '.join(vms)})
    print()
    print(f"\t Results saved to {output_file}")
    
def fetch_vms_data(api_url ,username, password,offset=0, limit=500):
    body = {
        "kind": "vm"}
    try:
        response = requests.post(api_url, params={'offset': offset, 'limit': limit},auth=(username, password),verify=False, headers={'Content-Type': 'application/json'}, data=json.dumps(body))
        print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception:
        print()
        if response.status_code == 401:
            print("\t Status Code:",response.status_code,",Please check your credentials!")
            
        #print(f"Failed to fetch data from ")
        return None


def parse_and_write_to_csv(data, csv_writer):
    res = []
    for entity in data.get('entities', []):
        cluster_name = entity.get('status', {}).get('cluster_reference', {}).get('name', '')
        vm_name = entity.get('status', {}).get('name', '')
        nics = entity.get('status', {}).get('resources', {}).get('nic_list', [])
        
        for nic in nics:
            mac = nic.get('mac_address', '')
            network_name = nic.get('subnet_reference', {}).get('name', '')
            csv_writer.writerow([cluster_name, vm_name,network_name,mac])
            res.append([cluster_name, vm_name,network_name,mac])

    return res
    #print(res)
    

def main():
    print()
    offset = 0
    limit = 500
    output_csv = "vms_macaddr.csv"

    with open("creds.csv","r") as creds:
        reader = csv.reader(creds)
        for row in reader:
            username = row[0]
            password = row[1]

    
    with open(output_csv, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Cluster Name', 'VM Name', 'Network Name','MAC Address'])
        with open("pc.csv","r") as pcs:
            reader = csv.reader(pcs)
            all_res=[]
            for row in reader:
                pc = row[0]
                api = f"https://{pc}:9440/api/nutanix/v3/vms/list"

                while True:
                    data = fetch_vms_data(api, username, password, offset, limit)
                    if data is None:
                        print("\t Failed to fetch data from ",pc)
                        print()
                        break
                    res = parse_and_write_to_csv(data, csv_writer)
               
                    all_res+=res
                    if len(data.get('entities', [])) < limit:
                        break

                    offset += limit
            print()
            print('\t All VMs MAC addresses saved in vms_macaddr.csv')
            print()
            duplicates = find_duplicate_macs(all_res)


            print_duplicates(duplicates)


            write_duplicates_to_csv(duplicates, 'duplicate_mac_addresses.csv')




output_csv = 'vms_data.csv'

if __name__ == "__main__":
   

    main()
