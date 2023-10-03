"""
Created on September 23 07:31:23 2023

@author: LK
"""

import xml.etree.ElementTree as ET
import gzip
import os
import re


#In case the events file can not be found, you might need to add the full path of this directory
#os.chdir('/FULLPATH/Link Volume')

scenarios = ['SC1.0','SC2.0', 'SC3.0']

def vehicle_matches_pattern(vehicle_name):
    return re.match(r'^\d{3}', vehicle_name) is not None

# Define the links you're interested in
target_links = {"125775", "69438", "76921"}

for scenario_name in scenarios:
    link_counts = {link: {} for link in target_links}  # Dictionary to store counts per hour for each link
    #file_name = f'{scenario_name}_berlin-v5.5-10pct.output_events.xml.gz'
    file_name = f'{scenario_name}_berlin-v5.5-10pct.0.events.xml.gz'
    p = 0

    with gzip.open(file_name, 'rt') as f:
        print("file opened")
        for _, elem in ET.iterparse(f, events=('end',)):
            #if elem.tag == 'event' and elem.get('type') == "actend":
            if elem.tag == 'event' and elem.get('type') == "entered link" and vehicle_matches_pattern(elem.get('vehicle')):
                link = elem.get('link')
                if link in target_links:
                    # Extract the hour from the event time
                    event_time = float(elem.get('time'))
                    hour = int(event_time // 3600)  # Convert seconds to hours

                    # Update the count for the specific link and hour
                    link_counts[link][hour] = link_counts[link].get(hour, 0) + 1

            p += 1
            if p % 1000000 == 0:
                print(f'Link Nr. {p} added for {scenario_name}')
            elem.clear()

    # Save the hourly results to a txt file for the current scenario
    with open(f'{scenario_name}_Link_Volume.txt', 'w') as f:
        for link, hourly_counts in link_counts.items():
            for hour, count in sorted(hourly_counts.items()):
                f.write(f'Link: {link}, Hour: {hour}, Count: {count}\n')

    print(f"Hourly results for {scenario_name} saved to {scenario_name}_Link_Volume.txt")
