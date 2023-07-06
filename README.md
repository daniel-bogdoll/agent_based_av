This document serves as an accompanying guide for the technical execution of the thesis: 

Sustainability of Autonomous Vehicles: An Agent-based Simulation of the Private Passenger Sector

In the submodule "matsim-berlin" find attached the forked version of the Open Berlin MATSim Scenario and adjustments made for the use case of the scenarios of the thesis

In the folger Data-Preparation find attached the python scripts to process the original input files of the Open Berlin Scenario to implement the above mentioned adjustments.

Necessary changes to make the scenarios work: https://github.com/daniel-bogdoll/matsim-berlin/tree/7c28ca12cc283561cd2b7236430d6381cc704ef6/scenarios/berlin-v5.5-1pct/input/drt

- Update config (local files instead of cloud based)
  
      Refer to locally stored network SHP, plans and vehicles file
  
- Update shape file (extend DRT range)
  
      Increase range so that all of the car links can now be used by DRT as well
  
- Update vehicles file (increase fleet size)
  
      Increase the number of vehicles (1,000 is the provided DRT baseline) according to the scenario and demand

- Update plans file (replace car trips with DRT trips)
  
      Iteratively go through the plan file to replace all plans for car travel, accoring to the scenario and demand, with DRT travel
