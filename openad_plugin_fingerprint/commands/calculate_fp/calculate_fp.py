# RDKit
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import rdFingerprintGenerator

# Data typing
from typing import Literal

# OpenAD
from openad.app.global_var_lib import GLOBAL_SETTINGS
from openad_tools.output import output_error, output_warning, output_text, output_success, output_table

#
#

# Define generators
generators = {
    "mfp": rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048),
    "rdk": rdFingerprintGenerator.GetRDKitFPGenerator(fpSize=2048),
    "ap": rdFingerprintGenerator.GetAtomPairGenerator(fpSize=2048),
    "tt": rdFingerprintGenerator.GetTopologicalTorsionGenerator(fpSize=2048),
    # Feature Morgan fingerprints are created using a Morgan generator which
    # uses a different method of assigning atom invariants (atom types)
    "fm": rdFingerprintGenerator.GetMorganGenerator(
        radius=2, fpSize=2, atomInvariantsGenerator=rdFingerprintGenerator.GetMorganFeatureAtomInvGen()
    ),
}

#
#


def calculate_fp(smiles: str, fp_type: Literal["mfp", "rdk", "ap", "tt", "fm"]):
    """Calculate the fingerprint of a molecule"""

    # Create RDKit molecule object
    rdkit_mol = Chem.MolFromSmiles(smiles)
    if rdkit_mol is None:
        output_error(f"Invalid SMILES string: <yellow>{smiles}</yellow>", return_val=False)
        return None

    # Select appropriate generator
    if fp_type not in generators:
        return output_error(
            f"Fingerprint type '{fp_type}' not recognized. Supported types are: {', '.join(generators.keys())}"
        )
    gen = generators[fp_type]

    # Generate fingerprint
    result = gen.GetFingerprint(rdkit_mol)

    # Return the fingerprint object
    return result


def fp_to_list(fp):
    """Convert an RDKit fingerprint object into a list"""
    bit_indices = list(fp.GetOnBits())
    return bit_indices


def list_to_fp(bit_indices):
    """Convert a fingerprint list to an RDKit fingerprint object"""
    fp = DataStructs.ExplicitBitVect(2048)
    for i in bit_indices:
        fp[i] = 1
    return fp
