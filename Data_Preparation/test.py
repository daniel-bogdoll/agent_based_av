import xml.etree.ElementTree as ET
import geopandas as gpd
from shapely.geometry import Point
import os
import matplotlib.pyplot as plt
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

# Read the Shapefile
data = gpd.read_file('/home/louis/Downloads/berlin.shp')

# Modify geometry
modified_data = data[:4]

# Save the modified Shapefile
filename = '/home/louis/Downloads/modified_berlin.shp'
modified_data.to_file(filename)

# Read the Shapefile
data3 = gpd.read_file(filename)

data3.plot()

plt.show()


'''
# Specify the path to your XML file
xml_file = '/home/louis/MA/berlin-drt-v5.5-1pct.output_plans.xml'

# Parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()
p = 0

for event, element in ET.iterparse(xml_file, events=('end',)):
        if element.tag == 'person':
            p += 1
            if p % 10000 == 0:
                print ("Nr.: " + str(p))
            legs = [elem for elem in element.iter() if elem.tag == 'leg'] # or elem.tag == 'activity']
            for i, leg in enumerate(legs):
                if leg.get('mode') == 'drt': 
                    print("Found 'drt' in the following line:")
                    print(line)'''