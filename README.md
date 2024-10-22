# poormans

Instructions: 
 - Every time the script is run, it will create a log file inside a folder named "epoch-data" as defined by DATA_FOLDER. The script will then compare the data file created at runtime with the data file from the previous epoch. 
 - If there are no data files for the previous epoch, the comparison will naturally not return any meaningful result.
 - The newspaper will be created inside the DATA_FOLDER following the name format poormans_epoch_XX.txt, where XX is the current epoch.

Requirements:
 - libra
 - Python 3.10 (other versions may or may not cause issues)
 
Usage: Simply call the script using Python ("python3 poormans_0.2.py")
 
License: This is provided under the GNU General Public License (GPL).

Disclaimer: This has been designed mostly as a personal pet project and is provided "as is."
