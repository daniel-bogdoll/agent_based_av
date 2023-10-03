"""
Created on September 27 23:44:57 2023

@author: LK
"""

import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import os
from matplotlib.ticker import ScalarFormatter

# Set default font for the entire plot
#plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10  # Adjust as needed


# Parse XML
tree = ET.parse(f'berlin-v5.5-network.xml')
root = tree.getroot()

# Extract node coordinates
print(f"Extracting node / link coordinates...")
nodes = {}
for node in root.findall(".//node"):
    node_id = node.get('id')
    x = float(node.get('x'))
    y = float(node.get('y'))
    nodes[node_id] = (x, y)

# Extract link coordinates
links = {}
for link in root.findall(".//link"):
    link_id = link.get('id')
    from_node = nodes[link.get('from')]
    to_node = nodes[link.get('to')]
    links[link_id] = (from_node, to_node)
print("Node / link coordinates extracted")

# Read Excel data
df = pd.read_excel('Heatmap_Hub_Links.xlsx')
print("Read excel with used links and create heatmap")


# Create a custom colormap
colors = [(1, 1, 1), (0, 0, 1), (1, 0, 0)]  # White -> Blue -> Red
cmap_name = 'custom_div_cmap'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Create a new figure for the current scenario
#fig, ax = plt.subplots(figsize=(5, 5))
fig = plt.figure(figsize=(8, 5))

# Adjust the width of the subplot to keep the plot size as 5x5
ax = fig.add_axes([0.25, 0.1, 0.5, 0.8])  # [left, bottom, width, height]


# Use LogNorm for normalization
norm = TwoSlopeNorm(vmin=0, vcenter=2, vmax=79)
for index, row in df.iterrows():
    link_id = str(row['link'])
    count = row['count']
    start, end = links[link_id]
    ax.plot([start[0], end[0]], [start[1], end[1]], color=cm(norm(count)), linewidth=0.5)


# Set x-axis and y-axis limits
ax.set_xlim(4570000, 4620000)
ax.set_ylim(5795000, 5845000)


# Adjust font size for tick labels
ax.tick_params(axis='both', which='major', labelsize=8)  # Adjust size as needed


# Add colorbar to the current subplot
sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.06, pad=0.04, shrink=0.4, aspect=30, anchor=(0.5, 0.2), panchor=(0.5, 0.2))
cbar.set_label('Vehicle Count', fontsize=8)
cbar.ax.tick_params(labelsize=8)  # Adjust size as needed


# Adjust layout to prevent overlap
fig.tight_layout()

# Save the heatmap for the current scenario as an image
#fig.savefig(f'Heatmap_Hubs.pdf', dpi=300, bbox_inches='tight')
fig.savefig(f'Heatmap_Hubs.pdf', bbox_inches='tight')
print(f'Heatmap saved as image')

# Close the current figure to free up memory
plt.close(fig)
