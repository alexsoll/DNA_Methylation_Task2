import numpy as np
import sys
import os

def get_dict():
    dict = {}
    file = open("annotations.txt", 'r')
    tmp = file.readline()
    while True:
        tmp = file.readline()
        if (len(tmp) == 0):
            break
        tmp = tmp.split("\t")
        dict[tmp[0]] = tmp[1:]
    print(len(dict))
    print(sys.getsizeof(dict) / (1024*1024))
    file.close()

def correct_data():  

    #        This function returns a dictionary with the original data, 
    #         among which data relating to the sex chromosomes 
    #          and the geo type Island and Shore were excluded.

    file = open("annotations.txt", 'r')
    dict = {}
    tmp = file.readline()
    while True:
        tmp = file.readline()
        if (len(tmp) == 0):
            break
        if (tmp.find("Island") == -1 and tmp.find("Shore") == -1):
            tmp = tmp.split("\t")
            if (tmp[1] != "X" and tmp[1] != "Y" and tmp[1] != '' and tmp[9] != '' and tmp[5] != ''):
                dict[tmp[0]] = tmp[1:]
            else:
                continue
        else:
            continue
    return dict

def get_dict_cpg_gene(dict):    #Creating a dictionary, where the key - cpg, data - genes
    dict_cpg_genes = {}
    for key in dict:
        dict_cpg_genes[key] = dict[key][4]
    return dict_cpg_genes

def get_dict_gene_cpg(dict):    #Creating a dictionary, where the key - gene, data - cpg
    #sorted(dict.items(), key = lambda item: item[1][4])
    dict_genes_cpg = {}
    for key in dict:
        tmp = dict[key][4].split(";")
        for j in range(len(tmp)):
            if tmp[j] not in dict_genes_cpg:
                dict_genes_cpg[tmp[j]] = key
            else:
                dict_genes_cpg[tmp[j]] += ";" + key
    return dict_genes_cpg


def get_value(cpg):
    file = open("average_beta.txt", 'r')
    sum = 0
    file.readline()
    total_sum = 0
    while True:
        tmp = file.readline()
        if (len(tmp) == 0):
            print("This cps not find!!!")
            break
        tmp = tmp.split()
        if tmp[0] != cpg:
            continue
        else:
            for i in range(1, len(tmp)):
                sum += float(tmp[i])
            total_sum = sum / (len(tmp) - 1)
            break
    return total_sum

def result_table():
    print("Wait, the operation is in progress ...")
    d = correct_data()
    cpg_gene = get_dict_cpg_gene(d)
    result_tab = {}
    file = open("average_beta.txt", 'r')
    file.readline()
    for line in file:
        line = line.split()
        if line[0] in cpg_gene:
            genes = cpg_gene.get(line[0])
            genes = genes.split(";")
            for i in range(len(genes)):
                if genes[i] not in result_tab:
                    result_tab[genes[i]] = line[1:]
                else:
                    for k in range(1, len(line)):
                        result_tab[genes[i]][k - 1] += ' ' + line[k]
        else:
            continue
    for key in result_tab:
        num_of_cpg = len(result_tab[key][0].split(" "))
        for i in range(len(result_tab[key])):
            sum = 0
            for j in range(num_of_cpg):
                tmp = result_tab[key][i].split(" ")
                sum += float(tmp[j])
            result_tab[key][i] = float(sum / num_of_cpg)
        

    file.close()
    return result_tab

def print_result_dict(dict):
    file = open("result.txt", "w")
    for key in dict:
        file.write(str(key) + '\t')
        for i in range(len(dict[key])):
            file.write(str(dict[key][i]) + " ")
        file.write("\n")
    clear = lambda: os.system('cls')
    clear()
    print("Done!  The data is saved in the file result.txt.")
    file.close()


def main():
    res = result_table()
    print_result_dict(res)


main()