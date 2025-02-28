---
title: Polarizability Trends in Group 14-16 Heteronuclear Molecules - A Computational Study
date: 2025-02-27 
tags: quantum chemistry, polarizability, computational chemistry, psi4, heteronuclear molecules
description: A systematic computational investigation of polarizability trends in diatomic molecules formed between Group 14 (C, Si, Ge, Sn, Pb) and Group 16 (O, S, Se, Te) elements, revealing how atomic size and electronic structure influence molecular response to electric fields.
---

## Abstract

This study presents a systematic computational investigation of polarizabilities in heteronuclear diatomic molecules formed from Group 14 (IVA) and Group 16 (VIA) elements. Using the finite field method implemented in Psi4 1.7, we calculated longitudinal polarizabilities for twenty molecular combinations (CO, CS, CSe, CTe, SiO, SiS, SiSe, SiTe, GeO, GeS, GeSe, GeTe, SnO, SnS, SnSe, SnTe, PbO, PbS, PbSe, PbTe). Results reveal clear periodic trends, with polarizability increasing both down Group 14 and across Group 16, reaching a maximum of 130.9 a.u. for PbTe. The data demonstrate that changes in the Group 16 element have a more pronounced effect on polarizability than changes in the Group 14 element. This work provides valuable insights into the electronic response properties of these molecular systems and establishes structure-property relationships that could guide materials design for applications requiring specific polarizability characteristics.

## Introduction

Molecular polarizability—the response of a molecule's electron density to an applied electric field—is a fundamental property that influences a wide range of physical and chemical phenomena, from intermolecular forces to optical properties.[@Jensen2017] Heteronuclear diatomic molecules present an interesting case study for polarizability analysis, as they exhibit directional responses that depend on the constituent atoms' electronic structures and the nature of the chemical bond between them.

Group 14 (C, Si, Ge, Sn, Pb) and Group 16 (O, S, Se, Te) elements form a diverse set of diatomic molecules with varying bond lengths, electronic configurations, and degrees of covalent/ionic character. As one moves down these groups in the periodic table, several important changes occur: increasing atomic size, more diffuse valence orbitals, and for the heavier elements, significant relativistic effects.[@Pyykko2012] These systematic variations make Group 14-16 combinations an ideal testbed for exploring how atomic properties translate into molecular polarizability trends.

The polarizability tensor component αzz (along the molecular axis) can be approximated through the numerical derivative approach known as the finite field method:[@Cohen1975]

$$\alpha_{zz} \approx \frac{\mu_z(F_z = +h) - \mu_z(F_z = -h)}{2h}$$

where h represents the applied electric field strength and μz is the z-component of the dipole moment. This approach provides a straightforward approximation of how the molecular dipole responds to an external electric field, from which polarizability can be derived.

Building upon our previous work on atomic polarizabilities of Group 14 elements, this study extends the investigation to heteronuclear molecules, with three primary objectives: (1) establishing a systematic dataset of molecular polarizabilities for Group 14-16 combinations, (2) identifying periodic trends and structure-property relationships, and (3) providing insights into the relative contributions of different elements to the overall molecular polarizability.

The results from this work not only enhance our fundamental understanding of electronic structure in heteronuclear systems but also have practical implications for materials design in applications ranging from nonlinear optics to molecular sensing.[@Nalwa2001]

## Experimental

### Computational Setup

Calculations were performed using Psi4 version 1.7 in a dedicated Conda environment on an Ubuntu 24.04 system. The project directory structure was organized as follows:

```bash
mkdir -p ~/projects/theo-chem/{inputs,outputs,scripts}
cd ~/projects/theo-chem
```

### Calculation Methodology

We employed the finite field method to calculate the longitudinal polarizability (αzz) of each molecule. This involved applying electric fields of +0.002, 0.0, and -0.002 atomic units along the molecular axis (z-direction) and measuring the resulting changes in the molecular dipole moment.

For each calculation, the Group 14 atom was placed at the origin, with the Group 16 atom positioned along the positive z-axis at the appropriate bond length. Bond lengths were estimated based on experimental and theoretical values from the literature, with adjustments made for the heavier elements.

### Python Implementation

The polarizability calculations were implemented in a Python script that automated the process for all molecular combinations. The script defined the molecular geometries, set appropriate basis sets for each element, handled the electric field perturbations, and calculated the polarizabilities from the dipole responses.

```python
import os
import psi4
import numpy as np

# Define elements from each group
group14 = ["C", "Si", "Ge", "Sn", "Pb"]
group16 = ["O", "S", "Se", "Te", "Po"]

# Define basis sets for each element
basis_sets = {
    # Group 14
    "C": "cc-pVDZ",
    "Si": "cc-pVDZ",
    "Ge": "cc-pVDZ",
    "Sn": "def2-svp",
    "Pb": "def2-svp",
    # Group 16
    "O": "cc-pVDZ",
    "S": "cc-pVDZ",
    "Se": "cc-pVDZ",
    "Te": "def2-svp",
    "Po": "def2-svp"
}

# Estimated bond lengths in Ångstroms (approximate values)
bond_lengths = {
    ("C", "O"): 1.13,   # CO
    ("C", "S"): 1.61,   # CS
    ("C", "Se"): 1.71,  # CSe
    ("C", "Te"): 1.95,  # CTe
    ("C", "Po"): 2.10,  # CPo (estimated)
    
    ("Si", "O"): 1.63,  # SiO
    ("Si", "S"): 2.00,  # SiS
    ("Si", "Se"): 2.06, # SiSe
    ("Si", "Te"): 2.32, # SiTe
    ("Si", "Po"): 2.47, # SiPo (estimated)
    
    ("Ge", "O"): 1.65,  # GeO
    ("Ge", "S"): 2.01,  # GeS
    ("Ge", "Se"): 2.14, # GeSe
    ("Ge", "Te"): 2.36, # GeTe
    ("Ge", "Po"): 2.51, # GePo (estimated)
    
    ("Sn", "O"): 1.84,  # SnO
    ("Sn", "S"): 2.21,  # SnS
    ("Sn", "Se"): 2.33, # SnSe
    ("Sn", "Te"): 2.53, # SnTe
    ("Sn", "Po"): 2.68, # SnPo (estimated)
    
    ("Pb", "O"): 1.92,  # PbO
    ("Pb", "S"): 2.29,  # PbS
    ("Pb", "Se"): 2.40, # PbSe
    ("Pb", "Te"): 2.60, # PbTe
    ("Pb", "Po"): 2.75  # PbPo (estimated)
}

# Define electric field strengths (in atomic units)
fields = [0.002, 0.0, -0.002]

# Directory setup
project_dir = "/home/peter/projects/theo-chem"
output_dir = os.path.join(project_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

def run_calculation(group14_element, group16_element, field):
    molecule_name = f"{group14_element}{group16_element}"
    job_name = f"{molecule_name}_field{field:+g}".replace("-", "minus")
    output_file = os.path.join(output_dir, f"{job_name}.out")
    
    # Get bond length in Bohr (convert from Ångstrom)
    bond_length = bond_lengths.get((group14_element, group16_element), 2.0) * 1.889725989
    
    # Set up Psi4
    psi4.core.set_output_file(output_file, False)
    psi4.set_memory('2 GB')
    
    # Define molecule - place group14 element at origin and group16 element along z-axis
    mol_string = f"""
    0 1
    {group14_element} 0.0 0.0 0.0
    {group16_element} 0.0 0.0 {bond_length}
    units bohr
    symmetry c1
    """
    
    molecule = psi4.geometry(mol_string)
    
    # Handle ECP elements
    needs_ecp = False
    if group14_element in ["Sn", "Pb"] or group16_element in ["Te", "Po"]:
        needs_ecp = True
        psi4.set_options({
            'puream': True,
            'df_basis_scf': 'def2-universal-jkfit'
        })
    
    # Set basis
    # Handle ECP elements and set basis sets correctly
    if needs_ecp:
        # Use def2-svp and def2-ecp for all atoms when any heavy element is present
        psi4.set_options({'basis': 'def2-svp'})
        
        # Set ECPs for specific elements
        if group14_element in ["Sn", "Pb"]:
            molecule.set_basis_by_symbol(group14_element, "def2-ecp", "ECP")
        if group16_element in ["Te", "Po"]:
            molecule.set_basis_by_symbol(group16_element, "def2-ecp", "ECP")
    else:
        # For molecules without ECPs, set the basis to the larger of the two basis sets
        # (This is a simplification - ideally we'd use mixed basis sets)
        psi4.set_options({'basis': basis_sets[group14_element]})
    
    # General calculation settings
    psi4.set_options({
        'scf_type': 'df',
        'e_convergence': 1e-8,
        'd_convergence': 1e-8,
        'maxiter': 150,      # Increase max iterations for potentially difficult convergence
        'guess': 'sad'       # Use superposition of atomic densities for initial guess
    })
    
    # Apply electric field if needed
    if field != 0.0:
        psi4.set_options({
            'perturb_h': True,
            'perturb_with': 'dipole',
            'perturb_dipole': [0.0, 0.0, field]  # Field along z-axis (molecular axis)
        })
    
    # Run the calculation
    try:
        energy, wfn = psi4.energy('scf', return_wfn=True)
        dipole = wfn.variable("SCF DIPOLE")
        print(f"Successfully calculated {molecule_name} with field {field}")
        print(f"Energy: {energy} Eh, Dipole: {dipole}")
        return dipole
    except Exception as e:
        print(f"Error in calculation for {molecule_name} with field {field}: {e}")
        return None

# Main workflow
results = {}
skip_elements = ["Po"]  # Polonium calculations might be problematic, skip if necessary

# Process each molecule combination
for g14 in group14:
    for g16 in group16:
        if g16 in skip_elements:
            continue
        
        molecule_name = f"{g14}{g16}"
        print(f"\nProcessing molecule: {molecule_name}")
        
        dipoles = {}
        for field in fields:
            dipole = run_calculation(g14, g16, field)
            if dipole is not None:
                dipoles[field] = dipole[2]  # Z-component (index 2) since molecule is along z-axis
        
        # Calculate polarizability using finite field method
        if len(dipoles) == 3:  # Ensure we have all three field strengths
            h = 0.002  # Field strength
            alpha_zz = (dipoles[0.002] - dipoles[-0.002]) / (2 * h)
            # Take absolute value for conventional reporting
            results[molecule_name] = abs(alpha_zz)
            print(f"Polarizability for {molecule_name}: {abs(alpha_zz):.4f} a.u.")

print("\nPolarizability results summary:")
print("Molecule | Polarizability (a.u.)")
print("---------|----------------------")
for molecule, alpha in sorted(results.items()):
    print(f"{molecule:7} | {alpha:.4f}")

# Create a 2D table for better visualization
print("\nPolarizability Matrix (Group 14 × Group 16):")
headers = [g16 for g16 in group16 if g16 not in skip_elements]
print(f"{'Element':<7} | " + " | ".join(f"{h:^7}" for h in headers))
print("-" * (8 + 10 * len(headers)))

for g14 in group14:
    row = f"{g14:<7} | "
    for g16 in group16:
        if g16 in skip_elements:
            continue
        molecule = f"{g14}{g16}"
        if molecule in results:
            row += f"{results[molecule]:7.4f} | "
        else:
            row += f"{'--':^7} | "
    print(row[:-2])  # Remove trailing " | "
```

### Basis Set Selection

Appropriate basis sets were selected based on the elements involved:
- For C, Si, Ge, O, S, and Se: cc-pVDZ basis sets were employed
- For Sn, Pb, and Te: def2-SVP basis sets with effective core potentials (ECPs) were used to account for relativistic effects

Polonium-containing compounds were excluded from this study due to the specialized relativistic treatment they would require and their limited practical relevance.

## Results

Our calculations yielded polarizability values for twenty different Group 14-16 diatomic molecules. The complete results are presented in Table 1.

**Table 1: Calculated Longitudinal Polarizabilities (α<sub>zz</sub>) for Group 14-16 Molecules**

| Molecule | Polarizability (a.u.) | Molecule | Polarizability (a.u.) |
|----------|----------------------:|----------|----------------------:|
| CO       | 12.21                 | GeO      | 29.02                 |
| CS       | 35.81                 | GeS      | 61.50                 |
| CSe      | 42.69                 | GeSe     | 75.70                 |
| CTe      | 59.46                 | GeTe     | 103.98                |
| SiO      | 27.84                 | SnO      | 38.23                 |
| SiS      | 59.98                 | SnS      | 73.20                 |
| SiSe     | 69.83                 | SnSe     | 90.72                 |
| SiTe     | 98.64                 | SnTe     | 123.34                |
| PbO      | 41.29                 | PbTe     | 130.91                |
| PbS      | 78.28                 | PbSe     | 96.42                 |

**Figure 1: 3D Surface Plot of Polarizabilities**

<img src="/images/polarizability_3d_surface.png" alt="3D Surface Polarizability">

**Figure 2: Heatmap of Polarizabilities Across Group 14-16 Combinations**

<img src="/images/polarizability_heatmap.png" alt="Polarizability Heatmap">

**Figure 3: Polarizability Trends for Group 14 Elements Across Group 16**

<img src="/images/polarizability_trends.png" alt="Polarizability Trends">

## Discussion

### Periodic Trends and Patterns

The results reveal several clear trends in the polarizabilities of Group 14-16 diatomic molecules:

1. **Increasing polarizability down Group 14:** 
   For a fixed Group 16 element, polarizability increases as we move from C to Pb. For example, with oxygen compounds: CO (12.21 a.u.) < SiO (27.84 a.u.) < GeO (29.02 a.u.) < SnO (38.23 a.u.) < PbO (41.29 a.u.). This trend reflects the increasing atomic size and more diffuse electron clouds of heavier Group 14 elements.

2. **Pronounced increase across Group 16:**
   For a fixed Group 14 element, polarizability increases dramatically as we move from O to Te. For carbon compounds: CO (12.21 a.u.) < CS (35.81 a.u.) < CSe (42.69 a.u.) < CTe (59.46 a.u.). The Group 16 element choice has a larger effect on polarizability than the Group 14 element, with increases of 3-4× when moving from O to Te compared to 2-3× when moving from C to Pb.

3. **Maximum values for heaviest combinations:**
   The highest polarizabilities are observed for the heaviest combinations, with PbTe (130.91 a.u.) showing approximately 10.7 times the polarizability of CO (12.21 a.u.).

4. **Non-linear progression:**
   The increase in polarizability is not strictly linear with atomic number, suggesting that factors beyond atomic size influence the electronic response properties.

### Structure-Property Relationships

Several structural factors correlate with the observed polarizability trends:

1. **Bond length effects:** 
   Longer bonds generally correlate with higher polarizabilities, as electron density is more diffuse and more easily distorted by external fields. The increasing bond lengths down both groups contribute to the overall polarizability increase.

2. **Valence electron contributions:**
   The more diffuse valence electron distributions in heavier elements lead to enhanced polarizability. This is particularly evident with Te compounds, which show dramatically higher polarizabilities than their O counterparts.

3. **Electronegativity differences:**
   The decreasing electronegativity difference between Group 14 and 16 elements for heavier combinations may allow for more symmetric electron distribution and greater polarizability.

### Comparison to Previous Work

Our results for the CO molecule (12.21 a.u.) align reasonably well with experimental values (~13-17 a.u.) and previous computational studies.[@Maroulis1996] The trend of increasing polarizability down groups is consistent with general chemical intuition and prior studies of atomic polarizabilities.

The relatively larger impact of Group 16 elements on polarizability compared to Group 14 elements is an interesting observation that warrants further investigation. This may relate to the greater variability in valence p-orbital diffuseness across the chalcogens compared to the Group 14 elements.[@Schwerdtfeger2002]

### Computational Considerations

The use of ECPs for heavier elements (Sn, Pb, Te) was essential for handling these calculations efficiently. Without proper treatment of relativistic effects, calculations for these elements would likely yield unreliable results. The absence of polonium compounds in our study reflects the additional computational challenges posed by very heavy elements, where even more sophisticated relativistic treatments would be necessary.

## Implications and Applications

The systematic dataset of molecular polarizabilities presented here has several potential applications:

1. **Nonlinear optical materials:**
   Molecules with high polarizabilities are candidates for nonlinear optical applications. Our results suggest that Te-containing compounds, particularly PbTe and SnTe, could be promising in this regard.

2. **Intermolecular force modeling:**
   Accurate polarizability values are essential for modeling dispersion forces and other non-bonded interactions in molecular simulations.

3. **Raman spectroscopy:**
   Polarizability derivatives determine Raman activity. The trends identified here could help predict relative Raman intensities across related molecules.

4. **Refractive index prediction:**
   Molecular polarizability directly relates to macroscopic refractive index, making these values useful for predicting optical properties of materials.

## Conclusion

This study has successfully mapped the polarizability landscape across twenty Group 14-16 diatomic molecules, revealing clear periodic trends and structure-property relationships. The polarizability increases both down Group 14 and across Group 16, with the heaviest combinations showing the highest values. Group 16 elements have a more pronounced effect on polarizability than Group 14 elements, suggesting that chalcogen selection is particularly important in designing materials with specific polarizability requirements.

The computational methodology employed here—combining the finite field approach with appropriate basis sets and ECPs—proved effective for systematically investigating these trends. This approach could be readily extended to other molecular systems and properties.

Future work could explore:

1. Higher-level calculations (MP2, CCSD) on select molecules to assess electron correlation effects on polarizability
2. Calculation of full polarizability tensors to examine anisotropy in the electronic response
3. Extension to polyatomic molecules containing Group 14 and 16 elements
4. Investigation of hyperpolarizability for these molecular systems, which is relevant for nonlinear optical applications
5. Incorporation of vibrational contributions to polarizability for comparison with experimental measurements

By establishing these fundamental structure-property relationships, this work contributes to our understanding of molecular electronic response properties and provides valuable insights for materials design in various technological applications.

## Acknowledgments

We acknowledge the contributions of the Psi4 development team and the Conda-Forge community for providing and maintaining the open-source tools that made this research possible.

## References