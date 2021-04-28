# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:24:49 2021

@author: Nick
"""

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

eths = [    "Mexican", "PuertoRican", "Cuban", "Dominican", "Costa Rican",
            "Guatemalan", "Honduran", "Nicaraguan", "Panamanian", "Salvadoran",
            "Argentinean", "Bolivian", "Chilean", "Colombian", "Ecuadorian",
            "Paraguayan", "Peruvian", "Uruguayan", "Venezuelan" ]

# Files for analysis.
zips = pd.read_csv( "flzips.csv", engine="python", index_col="ZIP" )
voterfile = pd.read_table( "dadecounty.txt", engine="python", names=vf_cols, dtype=str )

# Get the zipcode for analysis:
in_zip = str( input( "Enter Zipcode: "))

# Count the party aff's from the zipcode.
count_republicans = 
