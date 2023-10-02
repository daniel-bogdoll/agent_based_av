**Summary**

This document serves as a guide for the execution of the simulations and the processing of results related to the thesis: 

"Sustainability of Autonomous Vehicles: An Agent-based Simulation of the Private Passenger Sector"

In the submodule "submodule @7c28ca1" find the version of the Open Berlin MATSim Scenario that we used as a baseline.

In the folder Data-Preparation find the python scripts to process the original input files of the Open Berlin Scenario to generate input files that we used for our simulations.

The "input", RunBerlinScenario.java and RunDrtOpenBerlinScenario.java describe three files to adjust extracted from the OpenBerlinScenario

Overview of changes to input files that we made:

- Update config (local files with scenario settings)
   
- Update shape file (local files with extended DRT range)
  
- Update vehicles file (local files with increased fleet size)

- Update plans file (local files with car trips replaced by DRT trips)

- Update network file (local file which replaces car links by DRT mode based on the scenario setting)

With the newly generated input files, the scenarios as outlined in the thesis can be run



**Details about the Machine We Used for the 10% Scenarios**
- Operating System: Ubuntu 20.04.6 LTS
- CPU: Intel (R) Core (TM) i9-10900K CPU @ 3.70 GHz
- Memory size: 128 GiB



**Prerequisites**

- Java and Eclipse (or similar IDE)
	openjdk 11.0.20.1 2023-08-24 // Eclipse Version: 2023-06 (4.28.0)
	
- Python Packages Preprocessing
	import xml.etree.ElementTree as ET
	import pandas as pd
	import os
	import random
	from datetime import timedelta
	import copy
	import shutil
	import requests
	import gzip

- Python Packages Postprocessing 
	import pandas 
	import gzip
	import xml.etree.ElementTree 
	from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm 
	from matplotlib.ticker import ScalarFormatter 
	import gzip from collections 
	import defaultdict 
	import matplotlib.pyplot 
	import os 
	import matplotlib.colors 
	from matplotlib.colors 
	import PowerNorm 
	import re
	
- Other
	Font "Times New Roman" Installed on machine for heatmap generation		



**Step-By-Step Guide To Run (Default) MATSim Simulations on Your Machine**

- Install Java
	openjdk 11.0.20.1 2023-08-24
- Install Eclipse
	Version: 2023-06 (4.28.0)
- Clone MATSim Open Berlin Scenario 
	According to the attached submodule: https://github.com/daniel-bogdoll/matsim-berlin/tree/7c28ca12cc283561cd2b7236430d6381cc704ef6
- Set Up MATSim as a Maven project in Eclipse
	According to the attached submodule: https://github.com/daniel-bogdoll/matsim-berlin/tree/7c28ca12cc283561cd2b7236430d6381cc704ef6
- Open the following .java files in your IDE
	For non SAV scenarios: src/main/java/org/matsim/run/RunBerlinScenario.java
	For SAV scenarios: src/main/java/org/matsim/run/drt/RunDrtOpenBerlinScenario.java
	
- Execute either of the files for testing



**Step-By-Step Guide To Reproduce Scenarios from the Thesis**

- Clone the Data Preparation folder

Plans files
- Execute the "Plans_Demand_Forecast_Implementation.py" file to create the plans files that include travel demand increases 
- Run it 2 times in total: First set the forecast variable to "SC2", Second set the forecast variable to "SC3"
- Next, execute the "Plans_Manipulation.py" file to create all SAV scenario plans files
- Run it 3 times in total: First set the forecast variable to "SC1", Second set the forecast variable to "SC2", Third set the forecast variable to "SC3"
- You have now succesfully created all required plans files!

Network files
- Execute the "Network_Manipulation.py" file to create the three SAV-only network files used for all SAV scenarios
- You have now succesfully created all required network files!

- Clone the "Input" Folder of this Git Repository and replace the "Input" Folder in your matsim-berlin directory located at ./matsim-berlin/scenarios/berlin-v5.5-10pct/

Finalize Non SAV scenarios
- Move to folder ./input
- Copy&Paste the two plans files "berlin-v5.5-10pct_SC2.plans.xml.gz" and "berlin-v5.5-10pct_SC3.plans.xml.gz" into the /input folder to run the non-SAV scenarios

Finalize SAV scenarios
- Move to folder ./input/drt
- Update the directory in Line 171 of each config file by adding your filepath of the matsim-berlin clone (/ADJUSTACCORDINGTOYOURDIRECTORY/matsim-berlin/scenarios/berlin-v5.5-10pct/input/drt/SCX.X/berlin.shp)
- Note: It has to be the entire directory path of where your cloned matsim-berlin directory is located to avoid errors
- Move to each scenario folder (e.g. SC1.1)
- As noted in each readme file per scenario folder (e.g. SC1.1), copy&paste the according network and plans files into these folders
- E.g., copy&paste "berlin-v5.5-network_SCX.1.xml.gz" and "berlin-v5.5-10pct_SC1_SCX.1.plans.xml" from the Input_Processed and Input_Processed/10pct folder to the input/drt/SC1.1 folder 

Run Non SAV scenarios
- Clone the RunBerlinScenario.java file of this Git Repository
- Move to your local folder ./matsim-berlin/src/main/java/org/matsim/run and replace the RunBerlinScenario.java file
- You can now run the Non SAV scenarios by running this java file through Eclipse after commenting out the specific scenario to run in lines 78-80

Run SAV scenarios
- Clone the RunDrtOpenBerlinScenario.java file of this Git Repository
- Move to your local folder ./matsim-berlin/src/main/java/org/matsim/run/drt and replace the RunDrtOpenBerlinScenario.java file
- You can now run the SAV scenarios by running this java file through Eclipse after commenting out the specific scenario to run in lines 78-110


**Results**
- Processed Scenario results are documented in the folder Results 

**Reference**
- The MATSim Open Berlin Scenario as well as all mentioned .java files and unprocessed input files that we used for our analyses are based on the paper: https://www.sciencedirect.com/science/article/pii/S1877050919305848?via%3Dihub

