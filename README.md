

# VVER-1200 Assembly Comparison

This README describes the comparison of VVER-1200 nuclear reactor assembly simulations using Serpent and OpenMC.

## Overview

We conducted a comparison of the VVER-1200 assembly using two neutron transport codes: Serpent and OpenMC. The aim was to evaluate the consistency and performance of both tools in simulating the reactor assembly.

## Simulation Tools

- **Serpent**: A continuous-energy Monte Carlo reactor physics burnup calculation code. More information can be found on the [Serpent website](http://serpent.vtt.fi/).
- **OpenMC**: A community-developed, Monte Carlo particle transport simulation code. More information can be found on the [OpenMC website](https://openmc.org/).

## Key Findings

- **Neutron Flux Distribution**: Both Serpent and OpenMC provided similar neutron flux distributions across the VVER-1200 assembly.
- **Eigenvalue (k-eff) Calculations**: The k-eff values calculated by both codes were consistent and within acceptable limits.
- **Computational Performance**: OpenMC had a slightly better run-time performance compared to Serpent.

## Conclusion

The results show that both Serpent and OpenMC are reliable tools for simulating VVER-1200 assemblies, with minor differences in performance and output.

## References

- [Serpent website](http://serpent.vtt.fi/)
- [OpenMC website](https://openmc.org/)
