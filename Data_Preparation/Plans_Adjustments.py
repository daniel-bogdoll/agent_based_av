"""
Created on Tue May 23 16:21:45 2023

@author: LK
"""

import pandas as pd
import os
import xml.etree.ElementTree as ET
import shutil
import gzip
import requests

"""Define Database"""
database = "10pct"

"""Define Forecast"""
#forecast = "SC1"
forecast = "SC2"
#forecast = "SC3"

"""Define Scenario"""
scenario = ["SCX.1", "SCX.2", "SCX.3"]
j = 0








def extract_xml_gz(input_path, output_path):
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

"""Import Links (AV Zone) out of excel sheet"""
current_directory = os.getcwd()
directory_processed = os.path.join(current_directory, "Input_Processed")
directory_processed_10pct = os.path.join(current_directory, "Input_Processed", "10pct")
os.makedirs(directory_processed, exist_ok=True)

if forecast == "SC1":
    os.chdir(directory_processed_10pct)
    # Define the URL for the file to be downloaded
    url = "https://svn.vsp.tu-berlin.de/repos/public-svn/matsim/scenarios/countries/de/berlin/berlin-v5.5-10pct/input/berlin-v5.5-10pct.plans.xml.gz"

    # Download the file and save it locally
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        old_filename = "berlin-v5.5-" + database + "_" + forecast + ".plans.xml.gz"
        with open(old_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully and saved as {old_filename}!")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        exit()  # Exit the script if the download fails


for j in range(3):
    # Read the second sheet into a DataFrame
    os.chdir(directory_processed)
    xls = pd.ExcelFile(scenario[j] + '_links.xlsx')
    df = xls.parse(xls.sheet_names[0])

    # Convert the DataFrame to a list
    link_list = df.astype(str).values.tolist()

    #print(link_list)
    print("")

    # If the DataFrame consists of a single column, the list will be nested. Flatten it in this case:
    if df.shape[1] == 1:
        link_list = [item for sublist in link_list for item in sublist]

    """ Update leg mode in plans.xml based on links (AV Zone): car => AV; INCREMENTAL APPROACH TO SAVE MEMORY CAPACITY"""
    print("initiate new xml creation...")

    # Change the directory to "/Input_PreProcessed"
 
    os.chdir(directory_processed_10pct)

    p = 0

    # Example usage:
    input_gz_path = "berlin-v5.5-" + database + "_" + forecast + ".plans.xml.gz"
    old_filename = "berlin-v5.5-" + database + "_" + forecast + ".plans.xml"
    extract_xml_gz(input_gz_path, old_filename)
    filename = "berlin-v5.5-" + database + "_" + forecast + "_" + scenario[j] + ".plans.xml"

    h = 0
    k = 0

    with open(filename, 'w') as f:
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

        for event, element in ET.iterparse(old_filename, events=('end',)):
            if element.tag == 'person':
                p += 1
                if p % 10000 == 0:
                    print("Nr.: " + str(p))

                # Find leg and activity elements
                legs = [elem for elem in element.iter() if elem.tag == 'leg' or elem.tag == 'activity']
                
                # First pass: check if there's at least one leg that needs to be converted to "drt"
                move_to_next_person = False  # Flag to decide if we need to move to the next person
                for i, leg in enumerate(legs):
                    route = leg.find('.//route')
                    if (leg.get('mode') == 'car' or leg.get('mode') == 'ride') and (route.get('start_link') in link_list or route.get('end_link') in link_list or any(link in link_list for link in [[(link) for link in route.text.split()] if route.text else []])) and route.get('start_link') != route.get('end_link'):
                        move_to_next_person = False
                        break
                    else:  # This else block executes if the loop completed normally (no break statement encountered)
                        #if (leg.get('mode') == 'car' or leg.get('mode') == 'ride'):
                            #print("we are here")
                        move_to_next_person = True  # Set the flag to True as conditions are not met
                        # Break the inner loop
                if move_to_next_person == False:
                    # Second pass: if we're here, it means we've found a leg to convert. Now we convert all "car" / "ride" legs to "drt".
                    for i, leg in enumerate(legs):
                        route = leg.find('.//route')
                        if leg.get('mode') == 'car' or leg.get('mode') == 'ride':
                            leg.set('mode', 'drt')
                            attributes = element.findall('.//attribute[@name="routingMode"]')
                            for attribute in attributes:
                                attribute.text = 'drt'
                            route.set('type', 'drt')
                            route.attrib.pop('vehicleRefId', None)
                            # Remove existing text inside route element
                            route.text = None
                            
                            # Add new text inside route element
                            route.text = '300.0 208.7665374999924'
                            #print(str(p) + " updated")
                            
                        # Check if there is an activity element before the leg
                        if leg.tag == 'activity' and (leg.get('type') == 'car interaction' or leg.get('type') == 'ride interaction'):
                            leg.set('type', 'drt interaction')

                # Write the modified person element and its descendants to the new file
                f.write(ET.tostring(element, encoding='unicode'))

                # Clear the element and its descendants from memory once it's written
                element.clear()

        # Write the root element end tag manually
        f.write('</population>\n')

    print(f"plans file for scenario {database}, {scenario[j]}, {forecast} updated")
    
    j = j+1