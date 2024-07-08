import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openmc.deplete
import serpentTools
from tabulate import tabulate
from uncertainties import unumpy as unp
from matplotlib import pyplot
# Read Openmc results --------------------------------------------------------
results10 = openmc.deplete.ResultsList.from_hdf5("./depletion_results.h5")
# Obtain K_eff as a function of time
time, k = results10.get_eigenvalue()
deger10= k
time10= time
days10 = time10/(24*60*60)
# Read Serpent results -------------------------------------------------------
res10 = serpentTools.read('./vver_res.m')
serpent_days = res10.resdata['burnDays'][:, 0]
serpent_keff = unp.uarray(
    res10.resdata['absKeff'][:, 0],
    res10.resdata['absKeff'][:, 1]
)
serp10=res10.resdata['absKeff']
serz10=res10.resdata['burnup']
text='$\mathregular{^{241}Am}$'
pyplot.plot(serz10[:, 0], deger10[:, 0], label=f'OpenMC %10-{text}', color='red', marker='s',fillstyle='none',linewidth=0.5,markersize=3.5, linestyle='None')
pyplot.plot(serz10[:, 0], serp10[:, 0], label=f'Serpent %10-{text}', color='red',linewidth=1,markersize=3.5, linestyle='dashed')
plt.xlabel(r'$\bf{Burnup(MWd/kgU)}$', fontsize=10)
plt.ylabel(r'$\bf{K_{inf}}$', fontsize=10);
plt.yticks( weight='bold')
plt.xticks( weight='bold')
plt.legend(fontsize=10, loc='lower left', bbox_to_anchor=(1.0, 0.25), frameon=False, ncol=2, prop={'weight': 'bold'})
