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
![image](https://user-images.githubusercontent.com/75418624/202954626-21ac1906-913c-4238-b1a6-62d52f2ce538.png)
