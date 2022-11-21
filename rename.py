# -*- coding utf-8 -*-
"""
This pipeline is for changing the name of GCA file downloaded from NCBI database
Author:Xuhan Deng 
E-mail:dxh0222@gmail.com
date:2022.11.21
"""
# import pd
import sys
import os
import fnmatch
import gzip
import subprocess
import shutil
import pandas as pd


# function begin
def un_gz(file_name):  # this function is for unzip all .gz file in download from NCBI
    file_name_all = os.listdir(".")
    # acquire file name , remove suffix
    f_name = file_name.replace(".gz", "")
    # gzip file
    g_file = gzip.GzipFile(file_name)
    # read file(after gzip), write it in to same name file
    open(f_name, "wb+").write(g_file.read())
    g_file.close()


def all_path(dirname):  # this function is for unzip all file in all gzfile NCBI database
    for file in os.listdir(dirname):
        if fnmatch.fnmatch(file, "*.gz"):  # only process file with .gz suffix
            # print(file)
            abs = os.path.abspath(file)  # this process need absolute path
            un_gz(abs)  # call function un_gz


def read_report():  # read key line of report file(including isolate name and organism name)
    #    os.chdir(dirname)
    global organism
    global iso

    for file in os.listdir("."):  # read all name in Current folder
        if fnmatch.fnmatch(file, "*report.txt"):  # find report.txt file in all directoty
            # print(file)
            abs = os.path.abspath(file)  # return the absolute path of directory
            '''
            print(abs)
            print(type(abs))
            '''
            # retrieve organism name with shell script
            cat_orga = subprocess.Popen(["cat", abs], stdout=subprocess.PIPE)  # call shell script to cat the name
            grep_orga = subprocess.Popen(['grep', 'Organism name'], stdin=cat_orga.stdout,
                                         stdout=subprocess.PIPE, )  # call shell to grep organism name
            out_orga = grep_orga.stdout  # output content in shell script
            organism = out_orga.readline().decode('utf-8')  # output shell operation result to python

            # retrieve isolate name with shell script
            cat_iso = subprocess.Popen(["cat", abs], stdout=subprocess.PIPE)
            grep_iso = subprocess.Popen(['grep', 'Isolate'], stdin=cat_iso.stdout,
                                        stdout=subprocess.PIPE, )  # call shell to cat isolate name
            out_iso = grep_iso.stdout
            iso = out_iso.readline().decode('utf-8')  # output shell operation result

            # construct file name basic form is organism_name + isolate_name
            trimorg = organism.replace('Organism name:', '').replace('#', '').strip().replace(" ", "_")
            trimiso = iso.replace('#', '').replace('Isolate:', '').strip().replace(" ", '_')
            orga_iso = trimorg + '_iso_' + trimiso

    return orga_iso


# change file name
def renamefile(newname):
    tarfile = os.listdir(".")
    GCAlist = []
    for i in range(len(tarfile)):
        if fnmatch.fnmatch(tarfile[i], "GCA*"):
            GCAlist.append(tarfile[i])

    # print(GCAlist)
    # print("#####")
    # print(len(GCAlist))
    # print(len(rmfile))

    for i in range(len(GCAlist)):
        GCAlistsep = "_".join(GCAlist[i].split("_")[3:])
        # print(GCAlistsep)
        os.rename(GCAlist[i], newname + "_" + GCAlistsep)


def cpfile(faa_path, fna_path):  # move same type of directory to one file name
    current_location = os.listdir(".")
    for i in range(len(current_location)):
        if fnmatch.fnmatch(current_location[i], "*.fna"):
            if not "from" in current_location[i]:
                shutil.copy(os.path.abspath(current_location[i]), fna_path)
        else:
            pass
        if fnmatch.fnmatch(current_location[i], "*cds.faa"):
            shutil.copy(os.path.abspath(current_location[i]), faa_path)
        else:
            pass

#function end


# print(os.getcwd())

# an empty dataframe
ind = ["organism", "iso", "accession_number"]
csvout = pd.DataFrame(columns=ind)
# input a path
inp = "none"
if ("--input" in sys.argv):
    inp = sys.argv[sys.argv.index("--input") + 1]
in_dir = inp

# print('please input the path of director include all ncbi_folder')
# in_dir=input()
os.chdir(in_dir)
# create directory store file
if not os.path.exists("faa_file"):  # set a directory to store faa file
    os.makedirs("faa_file")
if not os.path.exists("fna_file"):  # set a directory to store fna file
    os.makedirs("fna_file")
faa_path = os.path.abspath("faa_file")
fna_path = os.path.abspath("fna_file")
dirlist = []
dirlist_pre = os.listdir()
for i in range(len(dirlist_pre)):
    if fnmatch.fnmatch(dirlist_pre[i], "GCA*"):
        dirlist.append(dirlist_pre[i])
# removeds. store in mac system, there always have a .ds_store file,author use these code to ignore them
# remove readme,txtfile
bek = []
for i in range(len(dirlist)):
    if '.DS_Store' in dirlist[i]:  # if .Ds_store in it ,put it in to bek
        bek.append(i)
    if fnmatch.fnmatch(dirlist[i], "*.txt"):
        bek.append(i)
dirlist = [dirlist[i] for i in range(len(dirlist)) if (i not in bek)]  # delate the element in bek[]
os.getcwd()
print('#################begin_for_looping#################')
for i in range(len(dirlist)):
    os.chdir(dirlist[i])  # enter operation dir
    dirname = os.path.abspath(".")
    all_path(dirname)
    new = read_report()

    # print(new)
    renamefile(new)
    cpfile(faa_path, fna_path)
    csvout.loc[i, 'organism'] = dirlist[i]
    csvout.loc[i, 'iso'] = organism
    csvout.loc[i, 'accession_number'] = iso
    os.chdir("../")  # back to last upper level dir
    os.rename(dirlist[i], new + "_" + dirlist[i])
csvout.to_csv("output.csv", header=True, sep=',')
