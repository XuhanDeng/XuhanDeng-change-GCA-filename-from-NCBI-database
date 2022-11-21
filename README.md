# XuhanDeng-change-GCA-filename-from-NCBI-database
change GCA filename
This script is for change the filename downloaded from NCBI database, it can process multiple files in one command line. first it will unzip all .gz file in all directories, and change all GCA filename with its organism name and isolate respectively, and it’s also create a table to record the accession number, organism name and the isolate.

reliance
pandas
fnmatch
gzip
subprocess
shutil

parameter
It’s just need you provide an absolute path of directory contain all folder downed from NCBI database.
please use parameter --input /User/*

input example
python rename.py --input /User/Xuhan_Deng/test

image example
input folder just like this 
 

After processing it will generate these
 

the file name is changed to this pattern
 

it also generates a table to record the accession number, isolate, organism
 
for next step analysis, it also retrieve all fna sequence file to faa_file directory and faa protein file to faa_file
 
![image](https://user-images.githubusercontent.com/75418624/202954437-f263c6e0-27b6-4d99-888c-dd0d1b0f1110.png)
