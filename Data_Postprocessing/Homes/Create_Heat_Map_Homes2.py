import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import PowerNorm
import os

#This needs to be commented out, in case you directory is already being recognized correctly
current_folder = os.getcwd() + "/Homes"
os.chdir(current_folder)

# Set default font for the entire plot and comment out, if Font Times New Roman available
plt.rcParams['font.size'] = 14 
#plt.rcParams["font.family"] = "Times New Roman"

def get_heatmap_data(filename, num_bins=10):
    # Load the data
    data = pd.read_csv(filename, delimiter=';', compression='gzip', header=None, dtype={0: str, 1: str, 2: str, 3: str, 5: str})

    data.columns = ['person', 'executed_score', 'first_act_x', 'first_act_y', 'first_act_type', 'income', 'subpopulation', 'home-activity-zone']

    # Convert the columns to numeric
    data['first_act_x'] = pd.to_numeric(data['first_act_x'], errors='coerce')
    data['first_act_y'] = pd.to_numeric(data['first_act_y'], errors='coerce')

    # Drop rows with NaN values
    data = data.dropna(subset=['first_act_x', 'first_act_y'])

    # Extracting the coordinates
    x = data['first_act_x']
    y = data['first_act_y']

    return x, y

scenario = ['SC1.0', 'SC2.0', 'SC3.0']

# Create a custom colormap that blends from white to viridis
colors = [(1, 1, 1)] + list(plt.cm.viridis(np.linspace(0, 1, 256)))
custom_colormap = mcolors.LinearSegmentedColormap.from_list("white_viridis", colors)

for i, sc in enumerate(scenario):
    file_name = f'{sc}_berlin-v5.5-10pct.output_persons.csv.gz'
    x, y = get_heatmap_data(file_name)
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=500)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Apply PowerNorm to the colormap
    gamma_value = 0.5  # Adjust this value to control the colormap's scale
    im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap=custom_colormap, aspect='auto', norm=PowerNorm(gamma=gamma_value, vmin=0, vmax=900))
    
    cbar_ax = fig.add_axes([0.25, -0.05, 0.5, 0.03])
    #ax.tick_params(axis='both', which='major', labelsize=8) 
    ax.set_xlabel("Longitude (EPSG:31468)", fontsize=14)
    ax.set_ylabel("Latitude (EPSG:31468)", fontsize=14)
    fig.colorbar(im, cax=cbar_ax, orientation='horizontal', label='Population Density (in Agents per Home Location)')

    plt.tight_layout()
    print(f'{sc} pdf saved')
    plt.savefig(f'{sc}_heatmap_home.pdf', bbox_inches='tight')
    plt.close(fig)
