import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

scenario = ['SC1.0', 'SC1.1', 'SC1.2', 'SC1.3']

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
    df = pd.read_excel(f'{scenario[k]}_heatmap_links.xlsx')
    print("Read excel with used links and create heatmap")


    # Create a custom colormap
    colors = [(1, 1, 1), (0, 0, 1), (1, 0, 0)]  # White -> Blue -> Red
    cmap_name = 'custom_div_cmap'
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

    # Create a new figure for the current scenario
    fig, ax = plt.subplots(figsize=(5, 5))

    # Use LogNorm for normalization
    norm = TwoSlopeNorm(vmin=-4000, vcenter=0, vmax=4000)
    for index, row in df.iterrows():
        link_id = str(row['link'])
        count = row['count']
        start, end = links[link_id]
        ax.plot([start[0], end[0]], [start[1], end[1]], color=cm(norm(count)), linewidth=0.1)


    # Set x-axis and y-axis limits
    ax.set_xlim(4560000, 4630000)
    ax.set_ylim(5785000, 5855000)

    ax.set_title(f'Vehicle Count Heatmap for {scenario[k]}')

    # Add colorbar to the current subplot
    sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.1, pad=0.1)
    cbar.set_label('Vehicle Count')

    # Adjust layout to prevent overlap
    fig.tight_layout()

    # Save the heatmap for the current scenario as an image
    fig.savefig(f'Heatmap_{scenario[k]}.png', dpi=300, bbox_inches='tight')
    print(f'Heatmap {scenario[k]} saved as image')

    # Close the current figure to free up memory
    plt.close(fig)
