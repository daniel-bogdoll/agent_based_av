Summary

This document serves as a guide for the execution of simulations and processing of results related to the thesis: 

"Sustainability of Autonomous Vehicles: An Agent-based Simulation of the Private Passenger Sector"

In the submodule "submodule @7c28ca1" find the version of the Open Berlin MATSim Scenario that we used as a baseline.

In the folder Data-Preparation find the python scripts to process the original input files of the Open Berlin Scenario to generate input files that we used for our simulations.

Overview of necessary changes to be made:

- Update config (local files with scenario settings)
   
- Update shape file (local files with extended DRT range)
  
- Update vehicles file (local files with increased fleet size)

- Update plans file (local files with car trips replaced by DRT trips)

- Update network file (local file which replaces car links by DRT mode based on the scenario setting)

With the newly generated input files, the scenarios as outlined in the thesis can be run



Details about the machine used for the 10% Scenarios
- Ubuntu 20.04.6 LTS
- CPU: Intel (R) Core (TM) i9-10900K CPU @ 3.70 GHz
- Memory size: 128 GiB



Prerequisites

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



Step-By-Step Guide To Run MATSim on Your Machine:

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
	
- Execute both files for testing



Step-By-Step Guide To Generate Scenarios of the Thesis




Results
- Processed results are documented in the folder Results 

Reference
- The MATSim Open Berlin Scenario that we used for our analyses is based on the paper: https://www.sciencedirect.com/science/article/pii/S1877050919305848?via%3Dihub



