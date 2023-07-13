import os

# Change the directory to "/Input_Processed"
directory = "/home/louis/MA/Input_Processed"
os.makedirs(directory, exist_ok=True)
os.chdir(directory)

# Save the workbook based on the date
filename = 'av_nodes_and_links.xlsx'
wb.save(filename)
print("Updated Excel saved")