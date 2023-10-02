import xml.etree.ElementTree as ET
import random
from datetime import timedelta
import copy
import pandas as pd
import gzip
import requests

"""Define Database"""
database = "10pct"

"""Choose moderate or high travel demand forecast"""
scenario = "SC2"
#scenario = "SC3"

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse_time(time_str):
    h, m, s = map(int, time_str.split(':'))
    total_minutes, rem_seconds = divmod(h * 60 * 60 + m * 60 + s, 60)
    total_hours, rem_minutes = divmod(total_minutes, 60)
    total_hours %= 24
    return timedelta(hours=total_hours, minutes=rem_minutes, seconds=rem_seconds)

xls = pd.ExcelFile('departure_times.xlsx')
df = xls.parse(xls.sheet_names[0])

# Convert the DataFrame to a list
dep_time_list = df.astype(str).values.tolist()

# Define the URL for the file to be downloaded
url = "https://svn.vsp.tu-berlin.de/repos/public-svn/matsim/scenarios/countries/de/berlin/berlin-v5.5-10pct/input/berlin-v5.5-10pct.plans.xml.gz"

# Download the file and save it locally
response = requests.get(url, stream=True)
if response.status_code == 200:
    old_filename = "berlin-v5.5-10pct.plans.xml.gz"
    with open(old_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"File downloaded successfully and saved as {old_filename}!")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
    exit()  # Exit the script if the download fails

new_filename = f"Input_Processed/{database}/berlin-v5.5-{database}_{scenario}.plans.xml.gz"

# Use gzip.open to read the gzipped XML file
print("Start loading plans file")
with gzip.open(old_filename, 'rt') as f:  # <-- 'rt' mode to read as text
    tree = ET.parse(f)
root = tree.getroot()
print("Finished loading plans file")

# Find all 'person' elements in the XML with integer IDs
persons = [person for person in root.findall('.//person') if is_int(person.attrib['id'])]

# Print out the total number of persons
print(f"Total number of persons: {len(persons)}")

# Calculate the number of persons to be added as 15% of the existing population
if scenario == "SC2":
    num_new_persons = int(len(persons) * 0.0656)
elif scenario == "SC3":
    num_new_persons = int(len(persons) * 0.1489)

# Print out the to be added number of persons
print(f"Total number of added persons: {num_new_persons}")

# Generate unique IDs for new persons
new_id = 10000000000000000000

print("New person ids for added population are generated. The range is: " + str(new_id) + " to: " + str(new_id + num_new_persons))

# Randomly select that many persons from the existing population
selected_persons = random.sample(persons, num_new_persons)

# For each selected person
added_person_count = 0
for selected_person in selected_persons:
    # Create a deep copy
    new_person = copy.deepcopy(selected_person)

    # Set new 'id' for the copied person
    new_person.attrib['id'] = str(new_id)
    car_leg = False
    # calculate the dep_time_delta
    for leg in new_person.findall('.//leg'):
        if leg.get('mode') == 'car':
            random_dep_time = str(random.choice(dep_time_list)[0])

            dep_time_delta  = parse_time(leg.attrib['dep_time']) - parse_time(random_dep_time)

            car_leg = True
            break;

    for leg in new_person.findall('.//leg'):
        if 'dep_time' in leg.attrib and car_leg == True:
            original_dep_time = parse_time(leg.attrib['dep_time'])
            new_dep_time = (original_dep_time - dep_time_delta)
            leg.attrib['dep_time'] = f'{new_dep_time.seconds//3600:02}:{new_dep_time.seconds//60%60:02}:{new_dep_time.seconds%60:02}'
  
        route = leg.find('route')
        if route is not None and 'vehicleRefId' in route.attrib:
            # Update the vehicleRefId based on the new person id
            route.attrib['vehicleRefId'] = str(new_id)
  
    for leg in new_person.findall('.//activity'):
        if 'end_time' in leg.attrib and car_leg == True:
            original_dep_time = parse_time(leg.attrib['end_time'])
            new_dep_time = (original_dep_time - dep_time_delta)
            leg.attrib['end_time'] = f'{new_dep_time.seconds//3600:02}:{new_dep_time.seconds//60%60:02}:{new_dep_time.seconds%60:02}'

    #Add the copy to the XML
    root.append(new_person)

    #Update assisting variables
    new_id = new_id+1
    added_person_count += 1

    if added_person_count % 1000 == 0:
        print(added_person_count)

# Now you need to write the root back to a new XML file
tree._setroot(root)
tree.write(new_filename)
print("Additional population is added")

# Write the updated XML back to a new gzipped file
with gzip.open(new_filename, 'wt') as f:  # <-- 'wt' mode to write as text
    # Write the header
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n')
    f.write('\n')
    f.write('<population>\n')
    f.write('\n')
    f.write('\t<attributes>\n')
    f.write('\t\t<attribute name="coordinateReferenceSystem" class="java.lang.String">DHDN_GK4</attribute>\n')
    f.write('\t</attributes>\n')
    f.write('\n')
    f.write('\n')
    f.write('<!-- ====================================================================== -->\n')
    f.write('\n')
    f.write('\t')

    # Write the rest of the XML
    tree = ET.ElementTree(root)
    tree.write(f, encoding='unicode')

print("XML file with new population data has been written.")

# Use gzip.open to read and write the gzipped XML file for final changes
with gzip.open(new_filename, 'rt') as file:
    lines = file.readlines()

# The indices in Python are 0-based, so we subtract 1 from the line numbers
del lines[11:18]

# check if last line is </population>
if lines[-1].strip() != '</population>':
    lines.append('</population>\n')
elif lines[-1] != '</population>\n':
    # replace the indented line with one that's not indented
    lines[-1] = '</population>\n'

with gzip.open(new_filename, 'wt') as file:
    file.writelines(lines)

print("final changes to the xml file made")
