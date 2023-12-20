# Filename: PortscannerP1.py
# Author: Chasham Teja
# Course: ITSC203
"""Details: Build a python Banner Grabber

#Resources:“https://www.hackers-arise.com/post/2018/01/12/python-scripting-for-hackers-part-2-building-a-banner-grabbing-tool

"""

#!/usr/bin/env python3

import socket
import subprocess
from datetime import datetime
import threading


def grab_banner(ip, port):
    try:
        # Create a socket object
        s = socket.create_connection((ip, port), timeout=2)

        # Check if the port is an HTTP port
        if port == 80:
            # Send a HEAD request to get the HTTP banner
            s.send(b'HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n')

        # Receive up to 1024 bytes of data (banner) from the service
        banner = s.recv(1024).decode('utf-8')
        s.close()
        return banner.strip()

    except Exception as e:
        return None


def search_exploits(service):
    try:
        # Use searchsploit to find exploits for the given service
        result = subprocess.run(['searchsploit', service], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            exploits = result.stdout.strip()
            print(exploits)  # Print the searchsploit results
            return exploits
        else:
            print(f"Error running searchsploit: {result.stderr}")
            return None

    except Exception as e:
        print(f"Exception during searchsploit: {e}")
        return None


def scan_ports(target_ip, ports, thread_id):
    current_datetime = datetime.now().strftime('%m%d%Y_%H%M')
    filename = f'bannergrab_{current_datetime}_thread_{thread_id}.txt'

    with open(filename, 'w') as file:
        for port in ports:
            service = grab_banner(target_ip, port)

            if service:
                print(f"{target_ip} - {port} - {service}")
                file.write(f"{target_ip} - {port} - {service}\n")

                exploits = search_exploits(service)
                if exploits:
                    file.write(f"Exploits found for {service}:\n{exploits}\n")


def main():
    # Specify the IP addresses to scan
    ip_addresses = ['192.168.100.5', '10.0.2.4']

    # Define a range of ports to scan (adjust as needed)
    ports_to_scan = range(1, 65000)

    # Create and start three threads for concurrent scanning
    threads = []
    for i, ip_address in enumerate(ip_addresses):
        thread = threading.Thread(target=scan_ports, args=(ip_address, ports_to_scan, i + 1))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
