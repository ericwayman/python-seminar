#bat_avg_model.py
#this is for one player.  Later we'll update it to get the priors for all the players
"""
A model for an MCMC model for batting average
"""

import pymc
import numpy as np
import pandas as pd

#load in the data
april_df = pd.read_table('./hw_11_data/laa_2011_april.txt',sep='\t')
at_bats = april_df['AB']
num_players = len(april_df.index)
num_hits = april_df['H']

#prior dist
mean_ba = .255
var_ba = .0011

a = ((1-mean_ba)/var_ba - 1/mean_ba)*mean_ba**2
b = a*(1/mean_ba -1)
ba = pymc.Beta('ba',alpha=a,beta=b,size=num_players)

#model
@pymc.deterministic(plot=False)
def modeled_ba(ba=ba):
	return ba

#likelihood
hits = pymc.Binomial('hits',n=at_bats,p=modeled_ba,value=num_hits,observed =True)
#hits_i = pymc.Binomial('hits_i',n=1000,p=modeled_ba,value=800,observed =True)
