#!/usr/bin/env python3
import os
import subprocess
import sys
import re

# Vina executable path
vina_path = "/autogrow/autogrow/docking/docking_executables/vina/autodock_vina_1_1_2_linux_x86/bin/vina"

# Docking parameters
center_x = 17.254
center_y = 2.25
center_z = 20.083
size_x = size_y = size_z = 25
exhaustiveness = 8
num_modes = 5

# Receptor file
receptor = "target.pdbqt"

# Target molecules - UPDATED: all molecules 1 to 10
target_molecules = ["adme_molecule1.pdbqt", "adme_molecule2.pdbqt", "adme_molecule3.pdbqt", 
                   "adme_molecule4.pdbqt", "adme_molecule5.pdbqt", "adme_molecule6.pdbqt",
                   "adme_molecule7.pdbqt", "adme_molecule8.pdbqt", "adme_molecule9.pdbqt", 
                   "adme_molecule10.pdbqt"]

def create_output_directory():
    """Create output directory"""
    output_dir = "Top10_compounds_docking"  # UPDATED: New folder name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created output directory: {output_dir}")
    else:
        print(f"✅ Using existing output directory: {output_dir}")
    return output_dir

def run_vina_docking(ligand, output_dir):
    """Run Vina docking to get all poses in one PDBQT file"""
    ligand_name = os.path.splitext(ligand)[0]
    
    # Vina outputs all poses to one file
    all_poses_pdbqt = os.path.join(output_dir, f"{ligand_name}_all_poses.pdbqt")
    log_file = os.path.join(output_dir, f"{ligand_name}_docking.log")
    
    vina_cmd = [
        vina_path,
        "--receptor", receptor,
        "--ligand", ligand,
        "--center_x", str(center_x),
        "--center_y", str(center_y),
        "--center_z", str(center_z),
        "--size_x", str(size_x),
        "--size_y", str(size_y),
        "--size_z", str(size_z),
        "--out", all_poses_pdbqt,
        "--log", log_file,
        "--exhaustiveness", str(exhaustiveness),
        "--num_modes", str(num_modes),
        "--energy_range", "3"
    ]
    
    print(f"\n🔄 Running Vina docking: {ligand}")
    
    try:
        result = subprocess.run(vina_cmd, capture_output=True, text=True, timeout=2400)
        
        if result.returncode == 0:
            print(f"    ✅ Vina docking completed")
            return all_poses_pdbqt, log_file
        else:
            print(f"    ❌ Vina failed: {result.stderr}")
            return None, None
            
    except Exception as e:
        print(f"    ❌ Error: {str(e)}")
        return None, None

def extract_pose_scores(log_file):
    """Extract binding scores for each pose"""
    scores = {}
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        
        for line in content.split('\n'):
            if re.match(r'^\s*\d+\s+[-\d\.]+', line) and 'kcal/mol' in line:
                parts = line.split()
                if len(parts) >= 2:
                    pose_num = int(parts[0])
                    score = parts[1]
                    scores[pose_num] = score
        
        return scores
    except Exception as e:
        print(f"    ⚠️  Error reading scores: {e}")
        return {}

def split_poses_to_individual_files(all_poses_pdbqt, ligand_name, output_dir, scores):
    """
    Split the multi-model PDBQT into individual PDBQT files (one per pose)
    Then convert each to clean PDB
    """
    try:
        with open(all_poses_pdbqt, 'r') as f:
            content = f.read()
        
        # Split by MODEL keyword
        models = re.split(r'MODEL\s+(\d+)', content)
        
        individual_files = []
        
        # Process each model (skip first empty element)
        for i in range(1, len(models), 2):
            if i + 1 >= len(models):
                break
                
            model_num = int(models[i])
            model_content = models[i + 1]
            
            # Get binding score
            score = scores.get(model_num, "unknown")
            
            # Create individual PDBQT file for this pose
            pose_pdbqt = os.path.join(output_dir, f"{ligand_name}_pose{model_num}_{score}kcal.pdbqt")
            
            with open(pose_pdbqt, 'w') as outfile:
                # Write clean PDBQT content (just atoms, no MODEL/ENDMDL)
                lines = model_content.split('\n')
                atom_count = 0
                
                for line in lines:
                    line = line.strip()
                    if line.startswith(('ATOM', 'HETATM', 'ROOT', 'ENDROOT', 'BRANCH', 'ENDBRANCH', 'TORSDOF')):
                        outfile.write(line + '\n')
                        if line.startswith(('ATOM', 'HETATM')):
                            atom_count += 1
                    elif line.startswith('ENDMDL'):
                        break
            
            if atom_count > 0:
                print(f"    📄 Created: {os.path.basename(pose_pdbqt)} ({atom_count} atoms)")
                
                # Now convert this individual PDBQT to clean PDB
                pose_pdb = pose_pdbqt.replace('.pdbqt', '.pdb')
                convert_single_pdbqt_to_pdb(pose_pdbqt, pose_pdb, model_num, score)
                
                individual_files.append((pose_pdbqt, pose_pdb))
            else:
                print(f"    ❌ Pose {model_num}: No atoms found")
                if os.path.exists(pose_pdbqt):
                    os.remove(pose_pdbqt)
        
        return individual_files
        
    except Exception as e:
        print(f"    ❌ Error splitting poses: {str(e)}")
        return []

def convert_single_pdbqt_to_pdb(pdbqt_file, pdb_file, pose_num, score):
    """Convert a single-pose PDBQT file to clean PDB"""
    try:
        with open(pdbqt_file, 'r') as infile:
            lines = infile.readlines()
        
        with open(pdb_file, 'w') as outfile:
            # Clean PDB header
            outfile.write("REMARK   Single pose from AutoDock Vina\n")
            outfile.write(f"REMARK   Pose {pose_num} - Binding Affinity: {score} kcal/mol\n")
            outfile.write("REMARK   Clean PDB for Discovery Studio\n")
            
            atom_counter = 1
            for line in lines:
                if line.startswith(('ATOM', 'HETATM')):
                    # Clean the line - remove PDBQT stuff from columns 67+
                    clean_line = line[:66].rstrip()
                    
                    # Ensure proper atom numbering
                    if len(clean_line) >= 11:
                        # Replace atom number with sequential counter
                        clean_line = clean_line[:6] + f"{atom_counter:5d}" + clean_line[11:]
                        atom_counter += 1
                    
                    outfile.write(clean_line + '\n')
            
            outfile.write("END\n")
        
        print(f"    🎯 Converted: {os.path.basename(pdb_file)}")
        return True
        
    except Exception as e:
        print(f"    ❌ PDB conversion error: {e}")
        return False

def main():
    """Main function - separate PDBQT and PDB files for each pose"""
    print("🧪 AutoDock Vina - Top 10 Compounds Individual Pose Docking")  # UPDATED: Title
    print("🎯 All 10 molecules - separate PDBQT file + separate clean PDB file for each pose")  # UPDATED: Description
    print("=" * 80)  # UPDATED: Wider separator
    
    # Check files
    if not os.path.exists(vina_path):
        print(f"❌ Vina not found: {vina_path}")
        sys.exit(1)
    
    if not os.path.exists(receptor):
        print(f"❌ Receptor not found: {receptor}")
        sys.exit(1)
    
    # Check ligands
    available_ligands = [mol for mol in target_molecules if os.path.exists(mol)]
    if not available_ligands:
        print("❌ No target molecules found!")
        sys.exit(1)
    
    print(f"✅ Found ligands: {len(available_ligands)}/{len(target_molecules)} molecules")  # UPDATED: Better count display
    for ligand in available_ligands:
        print(f"   • {ligand}")
    
    if len(available_ligands) != len(target_molecules):
        missing = set(target_molecules) - set(available_ligands)
        print(f"⚠️  Missing molecules: {', '.join(missing)}")
    
    output_dir = create_output_directory()
    
    print(f"\n📋 Parameters:")
    print(f"   Grid center: ({center_x}, {center_y}, {center_z})")
    print(f"   Grid size: {size_x}×{size_y}×{size_z} Å")
    print(f"   Poses per molecule: {num_modes}")
    print(f"   Total molecules: {len(available_ligands)}")  # UPDATED: Added molecule count
    
    print(f"\n🚀 Starting individual pose generation for all compounds...")
    print("=" * 80)
    
    total_individual_files = 0
    successful_molecules = 0
    
    for i, ligand in enumerate(available_ligands, 1):  # UPDATED: Added counter
        ligand_name = os.path.splitext(ligand)[0]
        print(f"\n📋 Processing {ligand} [{i}/{len(available_ligands)}]")  # UPDATED: Added progress counter
        
        # Step 1: Run Vina docking
        all_poses_pdbqt, log_file = run_vina_docking(ligand, output_dir)
        
        if all_poses_pdbqt and os.path.exists(all_poses_pdbqt):
            # Step 2: Extract scores
            scores = extract_pose_scores(log_file)
            print(f"    📊 Extracted {len(scores)} pose scores")
            
            # Step 3: Split into individual files
            individual_files = split_poses_to_individual_files(all_poses_pdbqt, ligand_name, output_dir, scores)
            
            if individual_files:
                print(f"    ✅ Created {len(individual_files)} individual pose files")
                total_individual_files += len(individual_files)
                successful_molecules += 1
            else:
                print(f"    ❌ Failed to create individual files")
        else:
            print(f"    ❌ Docking failed for {ligand}")
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 FINAL RESULTS - TOP 10 COMPOUNDS DOCKING")  # UPDATED: Title
    print("=" * 80)
    print(f"🎯 Total individual pose files created: {total_individual_files}")
    print(f"✅ Successful molecules: {successful_molecules}/{len(available_ligands)}")  # UPDATED: Success rate
    print(f"📁 Location: {output_dir}/")
    
    if total_individual_files > 0:
        print(f"\n📂 File Structure (examples):")
        print(f"   adme_molecule1_pose1_-8.2kcal.pdbqt  # Individual PDBQT")
        print(f"   adme_molecule1_pose1_-8.2kcal.pdb   # Clean PDB for DS") 
        print(f"   adme_molecule1_pose2_-7.8kcal.pdbqt")
        print(f"   adme_molecule1_pose2_-7.8kcal.pdb")
        print(f"   ... (up to pose{num_modes} for each molecule)")  # UPDATED: Dynamic pose count
        print(f"   adme_molecule2_pose1_-7.5kcal.pdbqt")
        print(f"   ... (continuing for all 10 molecules)")  # UPDATED: Reference to all 10
        
        print(f"\n💡 Discovery Studio Usage:")
        print(f"   ✅ Each .pdb file = ONE clean ligand")
        print(f"   ✅ No groups, no broken structures") 
        print(f"   ✅ Load any .pdb file individually")
        print(f"   ✅ Compare poses across all 10 compounds")  # UPDATED: Reference to all 10
        
        print(f"\n🔬 Analysis Tips:")
        print(f"   • Compare binding affinities across all 10 compounds")  # UPDATED: Reference to all 10
        print(f"   • Identify best-performing molecules by pose1 scores")
        print(f"   • Analyze interaction patterns across compound series")
    
    print(f"\n🏁 Top 10 compounds individual pose extraction completed!")  # UPDATED: Title

if __name__ == "__main__":
    main()
