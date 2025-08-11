# AutoGrow4-OXA23-Inhibitors: Computational Drug Discovery for β-Lactamase Inhibition

## Overview

This repository contains a computational drug discovery project using AutoGrow4's genetic algorithm to identify novel OXA-23 β-lactamase inhibitors. The study successfully evolved **1,250+ unique compounds** from 5 strategic seed ligands, discovering **MOLECULE1** as an optimal lead compound with superior binding affinity (-7.9 kcal/mol) and excellent pharmaceutical properties.

## Key Achievements

- **Lead Compound**: MOLECULE1 with exceptional ADME properties (11.66 score)
- **Clinical Superiority**: +0.8 to +2.1 kcal/mol improvement over existing inhibitors
- **Drug-like Properties**: 100% Lipinski compliance, zero toxicity alerts
- **Novel Scaffold**: 2-Hydroxypyridine β-lactam-sulfone hybrid framework

## Methodology

- **Target**: OXA-23 β-lactamase (PDB: 4K0X)
- **Algorithm**: AutoGrow4 genetic algorithm (32 generations)
- **Platform**: Docker containerization on Windows with Linux containers
- **Hardware**: Intel Pentium Silver N5030, 16GB RAM
- **Runtime**: 20 hours for complete evolution

## Strategic Seed Compounds

1. **Durlobactam** (FDA-approved 2023) - `CC1=C[C@@H]2CN(C(=O)N2OS(=O)(=O)O)[C@@H]1C(N)=O`
2. **Sulbactam** (Clinical standard) - `CC1([C@@H](N2[C@H](S1(=O)=O)CC2=O)C(=O)O)C`
3. **Benzylpenicillin** (Classical β-lactam) - `CC1([C@@H](N2[C@H](S1)[C@@H](C2=O)NC(=O)CC3=CC=CC=C3)C(=O)O)C`
4. **Clavulanic Acid** (Natural inhibitor) - `C[C@@H]1[C@H]([C@@H](C(=O)N1)CCO)O`
5. **Quinazoline Scaffold** (Novel heterocycle) - `CC1=NC=C(C=N1)OC2=NC3=C(C4=C(N3)C(=CC(=C4)F)NC)C(=N2)N`

## Repository Structure
AutoGrow4-OXA23-Inhibitors/
├── config/ # AutoGrow4 configuration files
├── input/ # Target preparation and seed compounds
├── output/ # AutoGrow4 evolutionary results
│ └── analysis/ # Generated CSV analysis files
├── admet_analysis/ # ADME-T property assessments
├── docking_results/ # Molecular docking analysis
└── docs/ # Detailed methodology and result


## Quick Start

### Prerequisites
- Docker Desktop
- 16GB RAM minimum
- 4+ CPU cores

### Installation
git clone https://github.com/[username]/AutoGrow4-OXA23-Inhibitors.git
cd AutoGrow4-OXA23-Inhibitors
docker-compose up

### Analysis
Pre-generated CSV files in `output/analysis/` ready for use with Python pandas, R, or Excel.

## Lead Compound (MOLECULE1)

- **SMILES**: `O=C([C@@H]1N2C(=O)C[C@H]2S(=O)(=O)C1(C)C)Nc1ncccc1O`
- **Binding Affinity**: -7.9 kcal/mol
- **ADME Score**: 11.66 (pharmaceutical-grade)
- **Solubility**: 15.3 mg/ml (exceptional)

## Citations

- **AutoGrow4**: Spiegel, J. O., & Durrant, J. D. (2020). *Journal of Cheminformatics*, 12(1), 25.
- **AutoDock Vina**: Trott, O., & Olson, A. J. (2010). *Journal of Computational Chemistry*, 31(2), 455-461.
- **RDKit**: Landrum, G. RDKit: Open-source cheminformatics. https://www.rdkit.org

*Complete citations available in [CITATIONS.md](CITATIONS.md)*

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

For questions or collaboration opportunities, please open an issue in this repository.

---

**Note**: This repository represents academic research. Experimental validation required before clinical applications.


