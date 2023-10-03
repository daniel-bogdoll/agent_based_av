"""
Created on  September 18 12:17:22 2023

@author: LK
"""

import xml.etree.ElementTree as ET
import pandas as pd
import gzip
from collections import defaultdict

"""Define scenario"""
scenario = ['SC1.3']

"""Events-FileName"""
file_name = f'{scenario[0]}_berlin-v5.5-10pct.output_events.xml.gz'


# Dictionaries to store request details and waiting times
request_details = {}
waiting_times = defaultdict(list)
p=0

# Open the gzipped XML file
with gzip.open(file_name, 'rt') as f:
    # Use iterparse for efficient parsing of large files
    for _, elem in ET.iterparse(f, events=('end',)):
        time_attr = elem.get('time')
        p += 1
        if p % 1000000 == 0:
            print(p)
        # Check if the time attribute exists and is not None
        if time_attr is not None:
            event_time = float(time_attr)
            
            # Only consider events within the timeframe 64800 and 72000
            if 64800 <= event_time <= 72000:
                event_type = elem.get('type')
                
                if event_type == "DrtRequest submitted":
                    request = elem.get('request')
                    person = elem.get('person')
                    from_link = elem.get('fromLink')
                    request_details[(request, person)] = {'time': event_time, 'fromLink': from_link}
                
                elif event_type == "PassengerRequest scheduled":
                    request = elem.get('request')
                    person = elem.get('person')
                    if (request, person) in request_details:
                        pickup_time = float(elem.get('pickupTime'))
                        delta = pickup_time - request_details[(request, person)]['time']
                        link = request_details[(request, person)]['fromLink']
                        waiting_times[link].append(delta)
        
        # Important: clear the element to free up memory
        elem.clear()

# Calculate average waiting times per link
average_waiting_times = {link: sum(times)/len(times) for link, times in waiting_times.items()}

# Convert to DataFrame
df = pd.DataFrame(list(average_waiting_times.items()), columns=['link', 'average'])

# Save to Excel
df.to_excel(f'{scenario[0]}_average_waiting_times.xlsx', index=False)
