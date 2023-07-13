# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:30:40 2023

@author: LK
"""

from pyproj import Proj, transform
import xml.etree.ElementTree as ET
from openpyxl import Workbook
import pandas as pd
import random
import os

"""
# Define the source CRS (WGS84 is the system used for GPS coordinates)
source_proj2 = Proj(init='epsg:4326')

# Define the target CRS
target_proj2 = Proj(init='epsg:31468')

# Function to convert a pair of latitude and longitude coordinates
def convert_coordinates2(lat, lon):
    x, y = transform(source_proj2, target_proj2, lon, lat)
    return x, y

#Define Boundaries of the polygon
lat_point1, lon_point1 = convert_coordinates2(52.482594, 13.327432)
lat_point2, lon_point2 = convert_coordinates2(52.535944, 13.327432)
lat_point3, lon_point3 = convert_coordinates2(52.535944, 13.459593)
lat_point4, lon_point4 = convert_coordinates2(52.508269, 13.459593)
lat_point5, lon_point5 = convert_coordinates2(52.482594, 13.393512)

# Calculate the cross product of two vectors to determine if a point is inside the pentagon
def cross_product(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1

def is_point_inside_pentagon(lat_a, long_a):
        
    # Check if the point is inside the pentagon using cross products
    cp1 = cross_product(lat_a - lat_point1, long_a - lon_point1, lat_point2 - lat_point1, lon_point2 - lon_point1)
    cp2 = cross_product(lat_a - lat_point2, long_a - lon_point2, lat_point3 - lat_point2, lon_point3 - lon_point2)
    cp3 = cross_product(lat_a - lat_point3, long_a - lon_point3, lat_point4 - lat_point3, lon_point4 - lon_point3)
    cp4 = cross_product(lat_a - lat_point4, long_a - lon_point4, lat_point5 - lat_point4, lon_point5 - lon_point4)
    cp5 = cross_product(lat_a - lat_point5, long_a - lon_point5, lat_point1 - lat_point5, lon_point1 - lon_point5)
    
    # Check if all cross products have the same sign (inside the pentagon) or not (outside the pentagon)
    if (cp1 >= 0 and cp2 >= 0 and cp3 >= 0 and cp4 >= 0 and cp5 >= 0) or (cp1 <= 0 and cp2 <= 0 and cp3 <= 0 and cp4 <= 0 and cp5 <= 0):
        return True
    else:
        return False

print('The Berlin Center Area in EPSG:31468 coordinates are defined ')
print("")
print("")

###Identify all nodes within that area###
######


#empty list for all nodes in Berlin Center Area, i = counter of nodes in AV Ban Area
node_list = []
i=0

for node in root.findall('.//node'):
    if is_point_inside_pentagon(float(node.get('x')), float(node.get('y'))):
        node_list.append(node.get("id"))
        print("Node added to the banned area: " + node.get("id"))
        i=i+1
        print("node nr.: " + str(i))
"""

###Identify all links within that area (either node starts or ends within defined area) and replace their mode of car by AV###
###And replace mode car by AV if in that area or add mode AV if mode car and not in AV area###
######

# Construct the file path using raw string or escaped backslashes
file_path = r'/home/louis/MA/Input_Preprocessed/berlin-v5.5-network.xml'  # Using raw string

# Check if the file path exists & Parse the XML file
if os.path.isfile(file_path): 
    tree = ET.parse(file_path)
    root = tree.getroot()

else:
    print(f"File not found: {file_path}")

# Read the Excel file and get the link IDs column as a list
link_list = []
df = pd.read_excel('/home/louis/MA/Input_Processed/drt_links.xlsx')
link_list = df['Link ID'].tolist()

j=0

for link in root.findall('.//link'):
    #if (link.get('id') not in link_list and not in link_list) and 'car' in link.get('modes').split(','):
    if link.get('id') not in link_list and 'car' in link.get('modes').split(','):

        #replace 'car' by 'AV' in Non-AV-Ban-Area
        modes = link.get('modes').split(',')
        #modes.remove('car')
        modes.append('drt')
        link.set('modes', ','.join(modes))
        print("link nr.: "+ str(link.get('id')) + " updated.")
print("All nodes and links updated")

# Change the directory to "/Input_Processed"
directory = "/home/louis/MA/Input_Processed"
os.makedirs(directory, exist_ok=True)
os.chdir(directory)

# Generate a filename for the new network.xml
filename = 'berlin-v5.5-network.xml'
tree.write(filename)

# Read the contents of the saved XML file
with open(filename, 'r') as file:
    xml_contents = file.read()

# Create the two lines to add at the beginning of the XML file
additional_lines = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">\n'

# Concatenate the additional lines with the XML contents
updated_xml_contents = additional_lines + xml_contents

# Write the updated contents back to the XML file
with open(filename, 'w') as file:
    file.write(updated_xml_contents)
    
print("Updated XML saved")
print("")