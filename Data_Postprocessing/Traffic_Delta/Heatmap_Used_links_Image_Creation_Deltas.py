import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import os

#This needs to be commented out, in case you directory is already being recognized correctly
current_folder = os.getcwd() + "/Traffic_Delta"
os.chdir(current_folder)

# Set default font for the entire plot and comment out, if Font Times New Roman available
plt.rcParams['font.size'] = 8
#plt.rcParams["font.family"] = "Times New Roman"

scenario = ['SC2.0','SC3.0','SC1.1', 'SC1.2', 'SC1.3']

for k in range(len(scenario)):
    # Parse XML
    tree = ET.parse(f'berlin-v5.5-network_{scenario[k]}.xml')
    root = tree.getroot()

    # Extract node coordinates
    print(f"Extracting node / link coordinates for {scenario[k]}...")
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
    df = pd.read_excel(f'Delta_{scenario[k]}.xlsx')
    print("Read excel with used links and create heatmap")

    # Create a custom colormap with sharper transition around the center value
    colors = [(0, 0.5, 0),   # Darker Green
              (0.5, 0.9, 0.5),   # Lighter Green
              (0.7, 0.7, 0.7),   # Light Gray
              (0.9, 0.5, 0.5),   # Lighter Red
              (0.5, 0, 0)]   # Darker Red
    positions = [0, 0.4, 0.5, 0.6, 1]
    cmap_name = 'custom_div_cmap'
    cm = LinearSegmentedColormap.from_list(cmap_name, list(zip(positions, colors)))

    # Use TwoSlopeNorm for diverging normalization
    if scenario[k] in ['SC1.1', 'SC1.2', 'SC1.3']:
        vmax=7500
        vmin=-7500
        norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
    else:
        vmax=1500
        vmin=-1500
        norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

    # Create a new figure for the current scenario
    fig, ax = plt.subplots(figsize=(5, 5))

    for index, row in df.iterrows():
        link_id = str(row['link'])
        count = row['count']
        start, end = links[link_id]
        if scenario[k] in ['SC1.1', 'SC1.2', 'SC1.3']:
            if abs(count) > 100:  # Define SOME_THRESHOLD based on what you consider as "slightly higher"
                lw = 0.6  # Original linewidth (0.4) + 0.2
            else:
                lw = 0.1
        else:
            if abs(count) > 50:  # Define SOME_THRESHOLD based on what you consider as "slightly higher"
                lw = 0.6  # Original linewidth (0.4) + 0.2
            else:
                lw = 0.1
        ax.plot([start[0], end[0]], [start[1], end[1]], color=cm(norm(count)), linewidth=lw)

    # Set x-axis and y-axis limits
    ax.set_xlim(4570000, 4620000)
    ax.set_ylim(5795000, 5845000)

    # Adjust font size for tick labels
    ax.tick_params(axis='both', which='major', labelsize=8)  # Adjust size as needed
    ax.set_xlabel("Longitude (EPSG:31468)", fontsize=8)
    ax.set_ylabel("Latitude (EPSG:31468)", fontsize=8)


    # Add colorbar to the current subplot
    sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.06, pad=0.08, shrink=0.4, aspect=30, anchor=(0.5, 0.2), panchor=(0.5, 0.2))
    cbar.set_label('Delta Vehicle Count per Street', fontsize=8)
    cbar.ax.tick_params(labelsize=8)  # Adjust size as needed

    # Save the heatmap for the current scenario as an image
    fig.savefig(f'Delta_heatmap_{scenario[k]}.pdf',bbox_inches='tight')
    print(f'Delta heatmap for {scenario[k]} saved as pdf')

    # Close the current figure to free up memory
    plt.close(fig)
