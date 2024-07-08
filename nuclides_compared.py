import matplotlib.pyplot as plt
import serpentTools
from openmc.data import ATOMIC_SYMBOL, zam
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openmc.deplete
import serpentTools
from tabulate import tabulate
from uncertainties import unumpy as unp
from matplotlib import pyplot
from math import pi

nuclides = ["U233","U235", "U238", "Th232", "Xe135", "Sm149", "Cs137", "I131", "Sr90", "Am241", "Am242", "Am244", "Np237", "Cm243", "Cm245", "Pu239", "Pu240", "Pu241"]
chem_list = ['$\mathbf{^{233}U}$','$\mathbf{^{235}U}$', '$\mathbf{^{238}U}$', '$\mathbf{^{232}Th}$', '$\mathbf{^{135}Xe}$', '$\mathbf{^{149}Sm}$', '$\mathbf{^{137}Cs}$', '$\mathbf{^{131}I}$', '$\mathbf{^{90}Sr}$', '$\mathbf{^{241}Am}$', '$\mathbf{^{242}Am}$', '$\mathbf{^{244}Am}$', '$\mathbf{^{237}Np}$', '$\mathbf{^{243}Cm}$', '$\mathbf{^{245}Cm}$', '$\mathbf{^{239}Pu}$', '$\mathbf{^{240}Pu}$', '$\mathbf{^{241}Pu}$']
text = ['$\mathbf{^{241}Am}$'] * len(nuclides)
softserp = 'Serpent'
softopn = 'OpenMC'
enrich10 = '%10-'

# Result OpenMC
radius = 0.38
volume = 312 * pi * radius**2
result10 = openmc.deplete.ResultsList.from_hdf5("./depletion_results.h5")

# Serpent verilerini okuma
res10 = serpentTools.read('./vver_res.m')
serpent_days10 = res10.resdata['burnDays'][:, 0]
burn=res10.resdata['burnup']
fuel10 = serpentTools.read('./vver_dep.m')['fuel']

for nuc, chem_symbol, text_item in zip(nuclides, chem_list, text):
    z, a, m = zam(nuc)
    time, atoms10 = result10.get_atoms('1', nuc)
    openmc_conc10 = atoms10 * 1e-24/volume
    serpent_conc10 = fuel10.getValues('days', 'adens', names=f'{ATOMIC_SYMBOL[z]}{a}{"m" if m else ""}')[0]
    plt.figure()  # nuclides figure
    plt.plot(burn[:, 0], openmc_conc10, color='red', marker='s', fillstyle='none', linewidth=0.5, markersize=3.5, linestyle='None', label=f'{softopn} {chem_symbol} {enrich10} {text_item}')
    plt.plot(burn[:, 0], serpent_conc10, color='red',linewidth=1, markersize=3.5, linestyle='dashed', label=f'{softserp} {chem_symbol} {enrich10} {text_item}')
    plt.xlabel(r'$\bf{Burnup(MWd/kgU)}$', fontsize=13)
    plt.ylabel(r'$\bf{Atom\ density(1/(barn*cm))}$', fontsize=13)
    plt.legend(fontsize=10, loc='lower left', bbox_to_anchor=(1.0, 0.25), frameon=False, ncol=2, prop={'weight': 'bold'})
    plt.yticks(weight='bold')
    plt.xticks(weight='bold')
    plt.title(f'{chem_symbol}',fontweight='bold')
    plt.show()
