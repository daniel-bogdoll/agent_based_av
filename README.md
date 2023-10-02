Summary

This document serves as an accompanying guide for the execution of simulations for the thesis: 

Sustainability of Autonomous Vehicles: An Agent-based Simulation of the Private Passenger Sector

In the submodule "submodule @7c28ca1" find attached the version of the Open Berlin MATSim Scenario that we used as a baseline

In the folder Data-Preparation find attached the python scripts to process the original input files of the Open Berlin Scenario and to generate input files that we used for our simulations.

Overview of necessary changes to be made:

- Update config (local files with scenario settings)
   
- Update shape file (local files with extended DRT range)
  
- Update vehicles file (local files with increased fleet size)

- Update plans file (local files with car trips replaced by DRT trips)

- Update network file (local file which replaces car links by DRT mode based on the scenario setting)

With the newly generated input files: Run the desired scenarios



Prerequisites
- 128 GB Ram
- Java and Eclipse (or similar IDE)
	openjdk 11.0.20.1 2023-08-24 // Eclipse Version: 2023-06 (4.28.0)
- Python Packages Preprocessing
- Python Packages Postprocessing
	import pandas
	import xml.etree.ElementTree
	from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
	from matplotlib.ticker import ScalarFormatter
	import gzip
	from collections import defaultdict
	import matplotlib.pyplot
	import os
	import matplotlib.colors
	from matplotlib.colors import PowerNorm


Step-By-Step Guide:

- Install Java
	openjdk 11.0.20.1 2023-08-24
- Install Eclipse
	Version: 2023-06 (4.28.0)
- Clone MATSim Open Berlin Scenario 
	According to the attached submodule: https://github.com/daniel-bogdoll/matsim-berlin/tree/7c28ca12cc283561cd2b7236430d6381cc704ef6
- Set Up MATSim as a Maven project in Eclipse
	According to the attached submodule: https://github.com/daniel-bogdoll/matsim-berlin/tree/7c28ca12cc283561cd2b7236430d6381cc704ef6
- Open .java Files
	For non SAV scenarios: src/main/java/org/matsim/run/RunBerlinScenario.java
	For SAV scenarios: src/main/java/org/matsim/run/drt/RunDrtOpenBerlinScenario.java
	
- Execute both files for testing

- Preprocessing:









- Install packages
- Set up Maven project
- Run RunDRTOpenBerlinScenario

Installation

Usage

Results

Paper citation



