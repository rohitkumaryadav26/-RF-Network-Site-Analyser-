# RF Network Site Analyser 
 
A Python tool that analyses 4G/5G telecom site performance using RSRP 
measurements. 
 
## What it does - Calculates Free Space Path Loss (FSPL) for each site - Classifies signal quality (Excellent / Good / Fair / Poor) - Generates a network health report with per-site statistics - Produces coverage curve graphs using NumPy and Matplotlib 
 
## Technologies 
Python 3, NumPy, Matplotlib 
 
## Telecom concepts used 
RSRP, FSPL, Link Budget, Signal Quality Classification (3GPP),
Coverage Curve Analysis, Drive Test Data Processing 

## Sites Analysed
| Site ID  | City       | Operator | Frequency | Quality   |
|----------|------------|----------|-----------|-----------|
| BLR_001  | Bengaluru  | Jio      | 3500 MHz  | Excellent |
| MUM_002  | Mumbai     | Airtel   | 1800 MHz  | Good      |
| DEL_003  | Delhi      | Vi       | 1800 MHz  | Poor      |
| CHN_004  | Chennai    | Jio      | 2600 MHz  | Good      |
 
## Project output 
![RSRP Comparison](site_rsrp_comparison.png) 
![Coverage Curves](coverage_curves_all_sites.png)

## Key Finding
DEL_003 (Delhi) has 80% poor readings — site flagged for
engineer action. Distance of 7.8 km from tower exceeds
acceptable coverage range for 1800 MHz at current power settings.
