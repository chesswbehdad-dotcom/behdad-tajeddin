import json
import csv

with open("devices.json", "r") as json_file:
    data = json.load(json_file)

total_devices = 0
hq_devices = 0
hq_rows = []

for device in data["results"]:
    dev_name = device["name"]
    role_name = device["role"]["name"]
    site_name = device["site"]["name"]
    platform_name = device["platform"]["name"]
    
    total_devices = total_devices + 1
    
    print(f"Device: {dev_name} | Role: {role_name} | Site: {site_name} | Platform: {platform_name}")
    
    if site_name == "HQ":
        hq_devices = hq_devices + 1
        hq_rows.append([dev_name, role_name, site_name, platform_name])

with open("devices_report.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["name", "role", "site", "platform"])
    for row in hq_rows:
        writer.writerow(row)

print(f"\nTotal devices: {total_devices}")
print(f"HQ devices: {hq_devices}")
