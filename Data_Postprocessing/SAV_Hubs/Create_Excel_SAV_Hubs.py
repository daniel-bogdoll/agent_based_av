"""
Created on September 26 08:57:04 2023

@author: LK
"""

import xml.etree.ElementTree as ET
from collections import defaultdict
from openpyxl import Workbook

# Load XML data from file
with open("/berlin-drt-v5.5.drt-10000vehicles-4seats.xml", "r") as file:
    xml_data = file.read()

# Parse the XML
root = ET.fromstring(xml_data)

# Extract start_link attributes and count occurrences
link_counts = defaultdict(int)
for vehicle in root.findall('vehicle'):
    start_link = vehicle.get('start_link')
    link_counts[start_link] += 1

# Create an Excel sheet
wb = Workbook()
ws = wb.active
ws.title = "Start Links"

# Add headers
ws.append(["link", "count"])

# Add data
for link, count in link_counts.items():
    ws.append([link, count])

# Save the Excel file
wb.save("Heatmap_Hub_Links.xlsx")
