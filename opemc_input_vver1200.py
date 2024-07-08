from math import pi, sqrt
import json
from pathlib import Path
import numpy as np
import openmc
import openmc.deplete

################################################################################
#  VODA-VODA ENERGY REACTOR 1200

#temperature_fuel = 534 + 273.15         # The VVER-1200 reactor
#temperature_structure = 432.5 + 273.15  # The VVER-1200 reactor
subassembly_pitch = 23.51             # The VVER-1200 reactor
subassembly_duct_outer = 23.310       # The VVER-1200 reactor
subassembly_duct_thickness = 0.1    # The VVER-1200 reactor
subassembly_duct_inner = subassembly_duct_outer - 2*subassembly_duct_thickness

void_radius = 0.08000
void1_radius = 0.38650
fuel_radius = 0.38000        # The VVER-1200 reactor
clad_inner_radius = 0.38650  # The VVER-1200 reactor
clad_outer_radius = 0.45500  # The VVER-1200 reactor
tube_inner_radius = 0.05450 # The VVER-1200 reactor
tube_outer_radius = 0.06000  # The VVER-1200 reactor

pin_pitch = 1.2750  # Table 12 from UAM document

################################################################################
# MATERIALS
# --- Lattice %1Am-241 ----------------------------
uo2 = openmc.Material(material_id=1, name='Am-241 %10')
uo2.add_nuclide('Th232', 0.00342122960573226)
uo2.add_nuclide('U234', 2.48879202510835E-06)
uo2.add_nuclide('U235', 0.000605806941976424)
uo2.add_nuclide('U238', 0.0116302283463303)
uo2.add_nuclide('O16', 0.0492259314770723)
uo2.add_nuclide('Pu238', 5.45198870587449E-05)
uo2.add_nuclide('Pu239', 0.00430563234067935)
uo2.add_nuclide('Pu240', 0.00134157738786715)
uo2.add_nuclide('Pu241', 0.000484903351116818)
uo2.add_nuclide('Pu242', 0.000190573843033255)
uo2.add_nuclide('Am241', 0.00257600524271674)
uo2.volume = 312 * pi * fuel_radius**2




helium = openmc.Material(material_id=2, name='Helium for gap')
helium.set_density('g/cm3', 0.001598)
helium.add_element('He', 2.4044e-4)

zircaloy = openmc.Material(material_id=3, name='Zircaloy 4')
zircaloy.set_density('g/cm3', 6.55)
zircaloy.add_element('Sn', 0.014  , 'wo')
zircaloy.add_element('Fe', 0.00165, 'wo')
zircaloy.add_element('Cr', 0.001  , 'wo')
zircaloy.add_element('Zr', 0.98335, 'wo')

borated_water = openmc.Material(material_id=4, name='Borated water')
borated_water.set_density('g/cm3', 0.740582)
borated_water.add_element('B', 4.0e-5)
borated_water.add_element('H', 5.0e-2)
borated_water.add_element('O', 2.4e-2)
borated_water.add_s_alpha_beta('c_H_in_H2O')

# % --- Thermal scattering data for light water:
# mat tube    -6.58000
# 40000.06c   -0.97500
# 41093.06c   -0.02500
mat_tube = openmc.Material(material_id=5, name='Mat tube')
mat_tube.set_density('g/cm3', 6.58000)
mat_tube.add_element('Zr', 0.97500  , 'wo')
mat_tube.add_element('Nb', 0.02500, 'wo')

################################################################################
# GEOMETRY
void1_outer = openmc.ZCylinder(r=void1_radius)
void_outer = openmc.ZCylinder(r=void_radius)
fuel_outer = openmc.ZCylinder(r=fuel_radius)
clad_outer = openmc.ZCylinder(r=clad_outer_radius)
tube_outer = openmc.ZCylinder(r=tube_outer_radius)
pin_universe = openmc.model.pin(
    [void_outer,fuel_outer,void1_outer, clad_outer],
    [helium,uo2,helium,zircaloy, borated_water]
)
guidetube_universe = openmc.model.pin(
    [fuel_outer,clad_outer],
    [borated_water,zircaloy, borated_water]
)
tube_universe = openmc.model.pin(
    [tube_outer],
    [mat_tube,borated_water]
 )

water_cell = openmc.Cell(fill=borated_water)
water_universe = openmc.Universe(cells=(water_cell,))
lattice = openmc.HexLattice()
lattice.center = (0., 0.)
lattice.pitch = (pin_pitch,)
lattice.orientation = 'x'
ring10=[pin_universe, pin_universe, pin_universe, pin_universe, pin_universe, pin_universe, pin_universe ,pin_universe, pin_universe, pin_universe]*6
ring9=[pin_universe, pin_universe, pin_universe, pin_universe, pin_universe, pin_universe, pin_universe ,pin_universe, pin_universe]*6
ring8=[pin_universe, pin_universe, pin_universe, pin_universe, pin_universe, pin_universe ,pin_universe, pin_universe]*6
ring7=[pin_universe, pin_universe, pin_universe, pin_universe, pin_universe ,pin_universe, pin_universe]*6
ring6=[pin_universe, pin_universe, pin_universe, guidetube_universe , pin_universe, pin_universe]*6
ring5=[guidetube_universe, pin_universe, pin_universe, pin_universe, pin_universe]*6
ring4=[pin_universe, pin_universe, pin_universe, pin_universe]*6
ring3=[pin_universe,pin_universe, guidetube_universe]*6
ring2=[pin_universe, pin_universe]*6
ring1=[pin_universe]*6
ring0=[tube_universe]
lattice.universes = [ ring10, ring9, ring8, ring7,ring6, ring5, ring4, ring3, ring2, ring1, ring0]
lattice.outer = water_universe

outer_hex = openmc.model.hexagonal_prism(
    subassembly_pitch / sqrt(3.),
    orientation='x',
    boundary_type='periodic'
)
duct_outer_hex = openmc.model.hexagonal_prism(
    subassembly_duct_outer / sqrt(3.), orientation='x')
duct_inner_hex = openmc.model.hexagonal_prism(
    subassembly_duct_inner / sqrt(3.), orientation='x')

lattice_cell = openmc.Cell(fill=lattice, region=duct_inner_hex)
duct = openmc.Cell(fill=zircaloy, region=~duct_inner_hex & duct_outer_hex)
outside_duct = openmc.Cell(fill=borated_water, region=~duct_outer_hex & outer_hex)

geom = openmc.Geometry([lattice_cell, duct, outside_duct])
geom.export_to_xml()
###############################################################################
#                     Transport calculation settings
###############################################################################

# Instantiate a Settings object, set all runtime parameters, and export to XML
settings = openmc.Settings()
settings.batches = 500
settings.inactive = 20
settings.particles = 6000

# Create an initial uniform spatial source distribution over fissionable zones
settings.source = openmc.source.Source(space=openmc.stats.Point())

###############################################################################
#                   Initialize and run depletion calculation
###############################################################################


# Get fission Q values from JSON file generated by get_fission_qvals.py
with open('/home/emil/data/depletion/serpent_fissq.json', 'r') as f:
    serpent_fission_q = json.load(f)

# Set up depletion operator
model = openmc.Model(geometry=geom, settings=settings)
chain_file = '/home/emil/data/depletion/chain_vver.xml'
op = openmc.deplete.Operator(model, chain_file,
    fission_q=serpent_fission_q,
    fission_yield_mode="average")

# cumulative steps in MWd/kg
burnup_cum = np.array([0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0, 92.5, 95.0, 97.5, 100.0])
burnup = np.diff(burnup_cum, prepend=0.0)
power = 131040  #312*420 W/cm Maximum fuel element linear power does not exceed 420 W/cm

# Perform simulation using the predictor algorithm
integrator = openmc.deplete.PredictorIntegrator(op, burnup, power, timestep_units='MWd/kg')
integrator.integrate()
