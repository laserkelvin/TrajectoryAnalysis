#/bin/python

import pandas as pd 
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import cm

""" Functions for analysis of molecular dynamics
    trajectories using Meredith's code.
"""

def PruneReactiveTrajectories(DataFrame):
    Threshold = DataFrame[DataFrame.keys()[0]] > 0.1
    DataFrame = DataFrame[Threshold]

def GatherData():
    """ Gather up all of the angular and kinetic energy
        data from OUT_ANG and OUT_VEL.

        This will only take data that have actually reacted.
        This is determined by seeing if the angular momentum
        of Fragment A is greater than 0.1.
    """
    JDF = pd.read_csv("OUT_ANG",
                      delim_whitespace=True,
                      usecols=[0,1],)
    KEDF = pd.read_csv("OUT_VEL",
                       delim_whitespace=True,
                       usecols=[0],)
    Combined = pd.concat([JDF, KEDF], axis=1)    # Combine the dataframes
    Threshold = Combined["J"] > 0.1              # and find ones that react
    Combined = Combined[Threshold]
    Combined.columns = ["Fragment A-J", "Fragment B-J", "Total Translational Energy"]
    Combined.to_csv("REACTIVE_DATA.csv")

class TrajectoryBatch:
    def __init__(self, CombinedData):
        self.Data = pd.read_csv(CombinedData, index_col=0)

    def PairPlot(self, size=5):
        Plot = sns.pairplot(self.Data, size=size)
        Plot.map_lower(sns.kdeplot, cmap=cm.viridis)
        Plot.map_upper(sns.kdeplot, cmap=cm.viridis)
        Plot.map_diag(plt.hist)