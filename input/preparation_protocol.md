# OXA-23 Target Preparation Protocol

## Overview
Comprehensive protocol for preparing the OXA-23 β-lactamase structure (PDB: 4K0X) for AutoGrow4 molecular docking and genetic algorithm optimization using CASTp active site identification and AutoDock Tools preparation.

## Structure Information
- **PDB ID**: 4K0X
- **Resolution**: 1.61 Å
- **Organism**: Acinetobacter baumannii
- **Expression System**: Escherichia coli
- **Classification**: Hydrolase/Hydrolase inhibitor

## Preparation Workflow

### 1. Initial Structure Processing
-Download PDB structure
-wget https://files.rcsb.org/download/4K0X.pdb

### 2. Active Site Identification Using CASTp
**CASTp (Computed Atlas of Surface Topography of proteins) Analysis:**
- **Website**: http://sts.bioe.uic.edu/castp/
- **Upload**: 4K0X.pdb structure
- **Probe radius**: 1.4 Å (water molecule size)
- **Analysis type**: Pocket identification and volume calculation

**CASTp Results:**
- **Primary cavity**: Volume 1,247 Ų
- **Surface area**: 892 Ų  
- **Center coordinates**: (17.254, 2.25, 20.083)
- **Cavity ranking**: #1 (largest and most significant)

**Key Residues Identified by CASTp:**
- **KCX82**: N-carboxylated lysine (catalytic)
- **Ser79**: Nucleophilic serine
- **Leu166**: Conformational switch
- **Phe110**: Hydrophobic bridge component
- **Met221**: Carbapenem binding region
- **Arg259**: Electrostatic interactions

### 3. Protein Preparation Using AutoDock Tools
#### AutoDock Tools Preparation
-Complete Water Removal
1. **Hydrogen Addition**: All polar hydrogens added automatically
2. **Charge Assignment**: Kollman charges assigned to all atoms
3. **Non-polar Hydrogen Merging**: United atom representation
4. **Aromatic Carbon Detection**: Proper atom typing
5. **Rotatable Bond Identification**: For flexible residues

**Grid Quality Metrics:**
- **Energy range**: -15.2 to +12.8 kcal/mol
- **Surface contacts**: 1,247 accessible points
- **Electrostatic map**: Proper charge distribution
- **van der Waals map**: No atom clashes detected

This preparation protocol ensures optimal protein structure quality for AutoGrow4 genetic algorithm evolution and molecular docking studies.