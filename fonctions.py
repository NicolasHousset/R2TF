#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:09:25 2019

@author: housset
"""
import sys

def readconf(filename):
    """
    Cette fonction lit un fichier de configuration
    contenant des lignes de la forme variable=valeur.
    Le caractère # est la marque d'un début de commentaire.
    Il peut y avoir des lignes vides dans ce fichier.

    La fonction reçoit en paramètre le nom du fichier.
    Elle renvoie un dictionnaire dont les clés sont les variables
    définies dans le fichier, et les valeurs leurs valeurs.
    """
    ...
    table = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line=="": continue
            if line[0]=="#": continue
            if not "=" in line:
                raise Exception(f"erreur de syntaxe en ligne")
            l = line.split('=')
            table[l[0]] = l[1]
        return table

def read_from_keyboard():
    """
    Renvoie des entiers lus au clavier
    """
    l =[]
    unAutre = True
    while(unAutre):   
        print("Entrez un nombre")
        a = int(input())
        l.append(a)
        print("Entrer un autre nombre ? (Y/N)")
        answer = input()
        unAutre = answer == "Y"
    return l

def read_from_cmdline():
    """
    Renvoie des entiers lus sur la ligne de commande
    """
    l = []
    if(len(sys.argv)>=2):
        for i in range(1,len(sys.argv)) :
            l.append(int(sys.argv[i]))
    return l

def read_from_file(filename):
    """
    Renvoie des entiers lus dans le fichier dont le nom est contenu dans filename
    """
    l =[]
    fichier = open(filename, 'r')
    line = fichier.readline()
    while line:
        # print(line)
        l.append(int(line.strip()))
        line = fichier.readline()
    fichier.close()
    return l

if __name__=="__main__":
  print("""
  Mode d'emploi
  """)