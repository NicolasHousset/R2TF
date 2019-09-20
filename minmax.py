#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:12:54 2019

@author: housset
"""

from fonctions import readconf
import fonctions

conf_file = "minmax.conf"

config = readconf(conf_file)

if config["read"]=="keyboard":
    l = fonctions.read_from_keyboard()
elif config["read"]=="arg":
    l = fonctions.read_from_cmdline()
elif config["read"]=="file":
    ...
    if "datafile" in config:
        l = fonctions.read_from_file(config["datafile"])
    else:
        print("Le chemin du fichier n'est pas défini")
    ...

if (config["search"]=="min"):
    print(min(l))
elif (config["search"]=="max"):
    print(max(l))
else:
    print("Erreur, fonction non reconnue")