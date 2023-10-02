"""
Created on Tue May 23 11:30:40 2023

@author: LK
"""
import xml.etree.ElementTree as ET
import pandas as pd
import os
import requests  # <-- Import the requests library
import gzip  # <-- Import the gzip module

"""Define Scenario"""
scenario = ["SCX.1", "SCX.2", "SCX.3"]
j = 0










# Construct the file path using raw string or escaped backslashes
current_directory = os.getcwd()
post_directory = os.path.join(current_directory, "Input_Processed")
file_name = "berlin-v5.5-network.xml.gz"  # <-- Updated to .xml.gz
file_path = os.path.join(file_name)

# Download the .xml.gz file
url = "https://svn.vsp.tu-berlin.de/repos/public-svn/matsim/scenarios/countries/de/berlin/berlin-v5.5-10pct/input/berlin-v5.5-network.xml.gz"
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"File downloaded successfully and saved as {file_path}!")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
    exit()  # Exit the script if the download fails

for j in range(3):

    # Check if the file path exists & Parse the gzipped XML file
    if os.path.isfile(file_path): 
        with gzip.open(file_path, 'rt') as f:  # <-- 'rt' mode to read as text
            tree = ET.parse(f)
            root = tree.getroot()
    else:
        print(f"File not found: {file_path}")

    # Read the Excel file and get the link IDs column as a list
    link_list = []
    df = pd.read_excel(f'{post_directory}/{scenario[j]}_links.xlsx')
    link_list = df['Link ID'].astype(str).tolist()

    i=0
    for link in root.findall('.//link'):
        #if (link.get('id') not in link_list and not in link_list) and 'car' in link.get('modes').split(','):
        if link.get('id') in link_list and 'car' in link.get('modes').split(','):
            #replace 'car' by 'AV' in Non-AV-Ban-Area
            modes = link.get('modes').split(',')
            modes.remove('car')
            modes.remove('ride')
            modes.append('drt')
            link.set('modes', ','.join(modes))
            if i % 10000 == 0:
                print(f"link nr. {i}: {str(link.get('id'))} updated.")
            i+1
    print("All nodes and links updated")

    # Change the directory to "/Input_Processed"
    os.makedirs(post_directory, exist_ok=True)
    os.chdir(post_directory)

    # Generate a filename for the new network.xml.gz
    filename = f'berlin-v5.5-network_{scenario[j]}.xml.gz'  # <-- Updated to .xml.gz
    with gzip.open(filename, 'wt') as f:  # <-- 'wt' mode to write as text
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">\n')
        tree.write(f, encoding='unicode')

    print("Updated XML saved")
    print("")
    j = j + 1