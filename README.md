This document serves as an accompanying guide for the technical execution of the thesis: 

Sustainability of Autonomous Vehicles: An Agent-based Simulation of the Private Passenger Sector

In the submodule "matsim-berlin" find attached the forked version of the Open Berlin MATSim Scenario and adjustments made for the use case of the scenarios of the thesis

In the folger Data-Preparation find attached the python scripts to process the original input files of the Open Berlin Scenario to implement the above mentioned adjustments.

Necessary changes to make the scenarios work:

- Update config (local files instead of cloud based)
- Update shape file (extend DRT range)
- Update vehicles file (increase fleet size)
- Update plans file (replace car trips with DRT trips)
