<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VVER-1200 Assembly Comparison</title>
</head>
<body>
    <h1>VVER-1200 Assembly Comparison</h1>
    <p>This README describes the comparison of VVER-1200 nuclear reactor assembly simulations using Serpent and OpenMC.</p>

    <h2>Overview</h2>
    <p>We conducted a comparison of the VVER-1200 assembly using two neutron transport codes: Serpent and OpenMC. The aim was to evaluate the consistency and performance of both tools in simulating the reactor assembly.</p>

    <h2>Simulation Tools</h2>
    <ul>
        <li><strong>Serpent</strong>: A continuous-energy Monte Carlo reactor physics burnup calculation code. More information can be found on the <a href="http://serpent.vtt.fi/" target="_blank">Serpent website</a>.</li>
        <li><strong>OpenMC</strong>: A community-developed, Monte Carlo particle transport simulation code. More information can be found on the <a href="https://openmc.org/" target="_blank">OpenMC website</a>.</li>
    </ul>

    <h2>Key Findings</h2>
    <ul>
        <li><strong>Neutron Flux Distribution</strong>: Both Serpent and OpenMC provided similar neutron flux distributions across the VVER-1200 assembly.</li>
        <li><strong>Eigenvalue (k-eff) Calculations</strong>: The k-eff values calculated by both codes were consistent and within acceptable limits.</li>
        <li><strong>Computational Performance</strong>: OpenMC had a slightly better run-time performance compared to Serpent.</li>
    </ul>

    <h2>Conclusion</h2>
    <p>The results show that both Serpent and OpenMC are reliable tools for simulating VVER-1200 assemblies, with minor differences in performance and output.</p>

    <h2>References</h2>
    <ul>
        <li><a href="http://serpent.vtt.fi/" target="_blank">Serpent website</a></li>
        <li><a href="https://openmc.org/" target="_blank">OpenMC website</a></li>
    </ul>
</body>
</html>


