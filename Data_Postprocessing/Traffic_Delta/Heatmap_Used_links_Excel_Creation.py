"""
Created on September 14 15:23:55 2023

@author: LK
"""

import xml.etree.ElementTree as ET
import gzip
import pandas as pd
import re


#scenarios = ['SC1.0', 'SC1.1', 'SC1.2', 'SC1.3']
scenarios = ['SC2.0', 'SC3.0']

def vehicle_matches_pattern(vehicle_name):
    # Check if the vehicle name starts with 'drt' or 3 numbers
    return vehicle_name.startswith('drt') or re.match(r'^\d{3}', vehicle_name)

for scenario_name in scenarios:
    # Construct the file name for the current scenario
    file_name = f'{scenario_name}_berlin-v5.5-10pct.output_events.xml.gz'
    #file_name = 'events.xml.gz'
    link_counts = {}
    p = 0

    # Open the gzipped XML file
    with gzip.open(file_name, 'rt') as f:
        # Use iterparse for efficient parsing of large files
        for _, elem in ET.iterparse(f, events=('end',)):
            if elem.get('type') == "entered link" and vehicle_matches_pattern(elem.get('vehicle')):
                link = elem.get('link')
                link_counts[link] = link_counts.get(link, 0) + 1
                p += 1
                if p % 1000000 == 0:
                    print(f'Link Nr. {p} added for {scenario_name}')
            # Important: clear the element to free up memory
            elem.clear()

    result = [(link, count) for link, count in link_counts.items()]

    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(result, columns=['link', 'count'])

    # Save the DataFrame to an Excel file for the current scenario
    df.to_excel(f'{scenario_name}_heatmap_links.xlsx', index=False)

    print(f"Results saved to {scenario_name}_heatmap_links.xlsx")
