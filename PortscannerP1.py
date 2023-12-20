# Filename: PortscannerP1.py
# Author: Chasham Teja
# Course: ITSC203
"""Details: Build a port scanner in Python

#Resources:“https://thepythoncode.com/article/make-port-scanner-python
https://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
"""

#!/usr/bin/env python3

import socket
import threading
import netifaces

open_ports = []


def scan_ports(target, start_port, end_port):
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)

        sock.close()


def scan_interfaces():
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        try:
            addresses = netifaces.ifaddresses(interface)
            ipv4_address = addresses[netifaces.AF_INET][0]['addr']

            print(f"Scanning ports on {interface} ({ipv4_address})...")
            scan_ports(ipv4_address, 1, 65535)

            with open('openportsfound.txt', 'a') as file:
                file.write(f"Open ports on {interface} ({ipv4_address}): {open_ports}\n")

            open_ports.clear()  # Clear the list for the next interface
            print(f"Results written to openportsfound.txt\n")
        except (KeyError, IndexError):
            print(f"Could not retrieve information for {interface}.\n")


def main():
    # Create a thread for scanning interfaces
    scan_thread = threading.Thread(target=scan_interfaces)

    # Start the scanning thread
    scan_thread.start()

    # Wait for the scanning thread to complete
    scan_thread.join()


if __name__ == "__main__":
    main()
