import xml.etree.ElementTree as ET
import random
from datetime import timedelta

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

#Generate a random 10-digit number for the filename
rand_num = random.randint(1e9, 1e10-1)
old_filename = "Data_Preparation/Input_Preprocessed/1pct/berlin-v5.5-1pct.plans.xml"
new_filename = f"Data_Preparation/Input_Processed/1pct/berlin-v5.5-1pct.plans_modified_{rand_num}.plans.xml"

# Parse the XML file and get the root element
tree = ET.parse(old_filename)
root = tree.getroot()

# Find all 'person' elements in the XML with integer IDs
persons = [person for person in root.findall('.//person') if is_int(person.attrib['id'])]

# Print out the total number of persons
print(f"Total number of persons: {len(persons)}")

# Calculate the number of persons to be added as 15% of the existing population
num_new_persons = int(len(persons) * 0.203)

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
    # Create a copy
    new_person = ET.ElementTree(selected_person).getroot()
    # Add the copy to the XML


    added_person_count += 1
    if added_person_count % 100 == 0:
        print(added_person_count)

    # Set new 'id' for the copied person
    #old_id = selected_person.attrib['id']
    new_person.attrib['id'] = str(new_id)

    # Change 'dep_time' in each 'leg' element by a random time between 0 and 2 hours
    for leg in new_person.findall('.//leg'):
        if 'dep_time' in leg.attrib:
            original_dep_time = parse_time(leg.attrib['dep_time'])
            random_minutes = timedelta(minutes=random.randint(0, 2 * 60))
            new_dep_time = (original_dep_time + random_minutes) % timedelta(days=1)
            leg.attrib['dep_time'] = f'{new_dep_time.seconds//3600:02}:{new_dep_time.seconds//60%60:02}:{new_dep_time.seconds%60:02}'


    #selected_person.attrib['id'] = old_id
    new_id = new_id+1
    root.append(new_person)

print("Additional population is added")

# Write the updated XML back to a new file
with open(new_filename, 'w') as f:
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

with open(new_filename, 'r') as file:
    lines = file.readlines()

# The indices in Python are 0-based, so we subtract 1 from the line numbers
del lines[11:18]

# check if last line is </population>
if lines[-1].strip() != '</population>':
    lines.append('</population>\n')
elif lines[-1] != '</population>\n':
    # replace the indented line with one that's not indented
    lines[-1] = '</population>\n'

with open(new_filename, 'w') as file:
    file.writelines(lines)

print("final changes to the xml file made")