import xml.etree.ElementTree as ET
import re
import gzip

# Path to the XML file
scenario = ['SC2.1', 'SC2.2', 'SC3.1', 'SC3.2']

for k in range(len(scenario)):
    file_path = f'{scenario[k]}_berlin-v5.5-10pct.1.events.xml.gz'

    # Use a set to keep track of unique vehicle values
    vehicles = set()

    # Regular expression pattern to match values starting with 4 numbers
    pattern = re.compile(r'^\d{4}')

    p = 0

    # Open the gzipped XML file
    with gzip.open(file_path, 'rt') as f:
        # Create an iterator for parsing the XML file
        context = ET.iterparse(f, events=("start", "end"))
        
        # Iterate over the XML elements
        for event, elem in context:
            p+=1
            if p%10000000 == 0:
                print(f'Line: {p}')
            if event == "end" and elem.tag == "event":
                vehicle = elem.get('vehicle')
                if vehicle and pattern.match(vehicle):  # Check if the vehicle attribute starts with 4 numbers
                    vehicles.add(vehicle)
                # Clear the element to free memory
                elem.clear()

    # Print the number of unique vehicle values
    print(len(vehicles))
