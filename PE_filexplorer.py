# Filename: m3p3.py
# Author: Chasham Teja
# Course: ITSC203
"""Details: Write a Python program to analyze Portable Executable (PE) files (typically Windows executables and DLLs) in a
specified directory, extract key information about these files, and present the results in a structured table format
while handling non-PE files.
#Resources:
“Exploring PE Files with Python: Buffer Overflows.” Buffer Overflows |, 18 Aug. 2019, bufferoverflows.net/exploring-pe-files-with-python/.

"""
#!/usr/bin/env python3
import pefile
import os
from prettytable import PrettyTable
from datetime import datetime

machine_types = {
    0x0: 'Unknown',
    0x14c: 'Intel 386',
    0x162: 'MIPS R3000',
    0x166: 'MIPS R4000',
    0x168: 'MIPS little-endian',
    0x184: 'Hitachi SH3',
    0x1a2: 'Hitachi SH4',
    0x1c0: 'ARM',
    0x1c2: 'Thumb',
    0x1c4: 'ARM Thumb-2',
    0x1d3: 'AM33',
    0x1f0: 'PowerPC',
    0x1f1: 'PowerPCFP',
    0x200: 'Intel IA-64',
    0x266: 'M32R',
    0x268: 'M32R little-endian',
    0x284: 'MIPS64',
    0x366: 'MIPS64 little-endian',
    0x466: 'Alpha AXP',
    0x520: 'SH5',
    0x1660: 'Intel x64',
}

characteristics_flags = {
    0x0001: 'RELOCS_STRIPPED',
    0x0002: 'EXECUTABLE_IMAGE',
    0x0004: 'LINE_NUMS_STRIPPED',
    0x0008: 'LOCAL_SYMS_STRIPPED',
    0x0010: 'AGGRESSIVE_WS_TRIM',
    0x0020: 'LARGE_ADDRESS_AWARE',
    0x0080: 'BYTES_REVERSED_LO',
    0x0100: '32BIT_MACHINE',
    0x0200: 'DEBUG_STRIPPED',
    0x0400: 'REMOVABLE_RUN_FROM_SWAP',
    0x0800: 'NET_RUN_FROM_SWAP',
    0x1000: 'SYSTEM',
    0x2000: 'DLL',
    0x4000: 'UP_SYSTEM_ONLY',
    0x8000: 'BYTES_REVERSED_HI',
}
subsystem_types = {
    0: 'Unknown',
    1: 'Native',
    2: 'Windows GUI',

}


# Function to format the Characteristics field
def format_characteristics(char_flags):
    flags = []
    for flag, label in characteristics_flags.items():
        if char_flags & flag:
            flags.append(label)
    return ' | '.join(flags)

# Create a PrettyTable for the final output
output_table = PrettyTable()
output_table.field_names = [
    "Filename",
    "PE Header Offset",
    "PE Signature",
    "Machine",
    "Timestamp",
    "Characteristics",
    "Optional Magic",
    "Image Base",
    "Entry Point",
    "Subsystem",
    "DLL/EXE"
]

pe_files_directory = 'C:/Users/tejac/Downloads/expandPE/expandPE2'

pe_file_extensions = ['.exe', '.dll']

for filename in os.listdir(pe_files_directory):
    if os.path.isfile(os.path.join(pe_files_directory, filename)) and any(filename.endswith(ext) for ext in pe_file_extensions):
        try:
            pe = pefile.PE(os.path.join(pe_files_directory, filename))

            pehdr_offset = pe.DOS_HEADER.e_lfanew
            pesig = pe.NT_HEADERS.Signature
            machine = pe.FILE_HEADER.Machine
            machine_str = machine_types.get(machine, 'Unknown')
            timestamp = datetime.utcfromtimestamp(pe.FILE_HEADER.TimeDateStamp).strftime('%m/%d/%Y %H:%M:%S')
            characteristics = format_characteristics(pe.FILE_HEADER.Characteristics)
            optmagic = pe.OPTIONAL_HEADER.Magic
            image_base = hex(pe.OPTIONAL_HEADER.ImageBase)
            entry_point = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
            subsystem = pe.OPTIONAL_HEADER.Subsystem
            subsystem_str = subsystem_types.get(subsystem, 'Unknown')
            pe_type = "EXE" if pe.is_exe() else "DLL" if pe.is_dll() else "Unknown"

            output_table.add_row([filename, pehdr_offset, pesig, machine_str, timestamp, characteristics, optmagic,
                                  image_base, entry_point, subsystem_str, pe_type])

        except pefile.PEFormatError:
            print(f"Skipping non-PE file: {filename}")

print(output_table)
