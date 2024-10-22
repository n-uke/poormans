# poormans

Instructions: 
 - Everytime the script is ran, it will create a log file inside a folder named "epoch-data" as defined by DATA_FOLDER. Then, the script will compare the data file created at runtime with the data file from the previous epoch. 
 - If there are no data files for the previous epoch, the comparison will naturally not return any meaningful result.
 - The newspaper will be created inside the DATA_FOLDER following the name format poormans_epoch_XX.txt, where XX is the current epoch

Requirements:
 - libra
 - python 3.10 (other versions may or may not cause issues)
 
Usage: simply call the script using python ("python3 poormans_0.2.py")
 
License: this is provided under the GNU General Public License (GPL)
