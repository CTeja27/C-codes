# Filename: m3p2.py
# Author: Chasham Teja
# Course: ITSC203
#Details: A Python code that uses the dictionary provided below and presents the information using the prettytable module.
"""Resources:
https://www.w3schools.com/python/default.asp"""


import ipaddress
from prettytable import PrettyTable

# Given dictionary
computer_info = {
    "Comp477": ["Gigabyte", 9133.27, "70561924KIQqzw", "68.192.163.42/255.255.240.0"],
    "Comp678": ["Asus", 7264.42, "56024371IQCewb", "198.78.85.109/255.255.248.0"],
    "Comp894": ["Acer", 4564.22, "41928367UHPkxu", "192.167.55.136/255.255.240.0"],
    "Comp592": ["Dell", 9378.82, "20451398MFWusg", "192.167.86.14/255.255.255.128"],
    "Comp397": ["Acer", 8115.08, "74189306HKLvwu", "176.33.145.182/255.255.248.0"],
    "Comp697": ["Asus", 8941.52, "17892534DZOlru", "10.0.252.127/255.255.192.0"],
    "Comp966": ["Dell", 9539.92, "46193287TYIurw", "10.0.222.132/255.255.252.0"],
    "Comp964": ["Dell", 4274.43, "04237918UTSdkj", "200.3.34.67/255.255.192.0"],
    "Comp634": ["Google", 5182.86, "95430287FCQfbk", "68.192.177.108/255.255.192.0"],
    "Comp565": ["Toshiba", 1904.33, "57018243JPYtpu", "192.167.63.98/255.255.240.0"],
    "Comp906": ["Dell", 5228.37, "96134827IHGibu", "176.33.20.163/255.255.192.0"],
    "Comp481": ["Asus", 7790.58, "05793218BRZjgl", "198.78.237.73/255.255.248.0"],
    "Comp370": ["Dell", 9251.70, "89531276LIMqby", "68.192.129.199/255.255.192.0"],
    "Comp703": ["Toshiba", 7520.04, "53179426FUXqjz", "200.3.191.102/255.255.192.0"],
    "Comp493": ["Google", 4621.55, "06514398WINzou", "198.78.59.119/255.255.240.0"]
}

# Create a PrettyTable with column headers
table = PrettyTable(["Computer Name", "Manufacturer", "Asset Tag", "IP Address", "IP Subnet", "Price"])

# Lists to store IP addresses and subnets
ip_addresses = []
subnets = []

# Dictionary to store IP addresses in the same subnet
subnet_ip_dict = {}

# Iterate through the dictionary and extract information
for computer_name, info in computer_info.items():
    manufacturer, price, asset_tag, ip_info = info
    ip_network = ipaddress.IPv4Network(ip_info, strict=False)  # Parse IP Address and Subnet

    # Append IP address and subnet to respective lists
    ip_addresses.append(ip_network.network_address)
    subnets.append(ip_network)

    # Add information to the table
    table.add_row([computer_name, manufacturer, asset_tag, ip_network.network_address, ip_network.netmask, price])

    # Store IP addresses in the same subnet
    subnet_ip = str(ip_network.network_address)
    if subnet_ip in subnet_ip_dict:
        subnet_ip_dict[subnet_ip].append(computer_name)
    else:
        subnet_ip_dict[subnet_ip] = [computer_name]

# Display the table
print(table)

# List IP addresses that are in the same subnet
for subnet, computer_names in subnet_ip_dict.items():
    if len(computer_names) > 1:
        print(f"\nIP Addresses in the same subnet {subnet}/{subnets[0].prefixlen}:")
        print(", ".join(computer_names))
