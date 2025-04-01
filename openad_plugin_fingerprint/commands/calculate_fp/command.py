import os
import pyparsing as py

# OpenAD
from openad.core.help import help_dict_create_v2
from openad.smols.smol_functions import get_best_available_smiles

# OpenAD tools
from openad_tools.output import output_error, output_warning, output_text, output_success, output_table
from openad_tools.helpers import description_txt
from openad_tools.grammar_def import molecule_identifier_s, molecule_working_set

# Plugin
from openad_plugin_fingerprint.plugin_grammar_def import calculate, fp_type, f_or, clause_update
from openad_plugin_fingerprint.plugin_params import PLUGIN_NAME, PLUGIN_KEY, PLUGIN_NAMESPACE
from openad_plugin_fingerprint.commands.calculate_fp.calculate_fp import calculate_fp, fp_to_list


class PluginCommand:
    """Hello world demo command"""

    category: str
    index: int
    name: str
    parser_id: str

    def __init__(self):
        self.category = "Main"
        self.index = 0
        self.name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        self.parser_id = f"plugin_{PLUGIN_KEY}_{self.name}"

    def add_grammar(self, statements: list, grammar_help: list):
        """Create the command definition & documentation"""

        # Command definition
        statements.append(
            py.Forward(
                py.CaselessKeyword(PLUGIN_NAMESPACE)
                + calculate
                + py.Optional(fp_type)
                + f_or
                + (molecule_working_set | molecule_identifier_s)
                + clause_update
            )(self.parser_id)
        )

        # Command help
        grammar_help.append(
            help_dict_create_v2(
                plugin_name=PLUGIN_NAME,
                plugin_namespace=PLUGIN_NAMESPACE,
                category=self.category,
                command=[
                    f"{PLUGIN_NAMESPACE} calc [ <fp_type> ] for @mws [ update ]",
                    f"{PLUGIN_NAMESPACE} calc [ <fp_type> ] for <smiles>",
                    f"{PLUGIN_NAMESPACE} calc [ <fp_type> ] for [<smiles>,<smiles>,...]",
                ],
                description_file=description_txt(__file__),
            )
        )

    def exec_command(self, cmd_pointer, parser):
        """Execute the command"""

        cmd = parser.as_dict()
        # print(cmd)

        # parse identifiers
        from_mws = "mws" in cmd
        # A. from molecule working set
        if from_mws:
            smiles_list = [get_best_available_smiles(mol) for mol in cmd_pointer.molecule_list]
            if len(smiles_list) == 0:
                return output_error("No molecules in the working set")
        # B. from command
        else:
            smiles_list = cmd.get("identifiers")

        # Parse command arguments
        is_single = len(smiles_list) == 1
        fp_type = cmd.get("fp_type", "mfp")  # Default fingerprint type is Morgan
        udpate_mws = "update" in cmd

        # Calculate fingerprint for each SMILES string
        results = []
        for i, smiles in enumerate(smiles_list):
            fp = calculate_fp(smiles, fp_type)
            results.append(fp)

            # Update molecule working set if requested
            if from_mws and udpate_mws:
                mol = cmd_pointer.molecule_list[i]
                mol.get("properties", {})[f"fp_{fp_type}"] = fp_to_list(fp)

                # Log
                mol_name = mol.get("name") or get_best_available_smiles(mol)
                if fp:
                    output_success(f"{i:>3}: fp_{fp_type} saved for for molecule: {mol_name}")
                else:
                    output_error(f"{i:>3}: No fp_{fp_type} available for molecule: {mol_name}")

        # Return a single result or a list of results
        if is_single:
            return results[0]
        else:
            return results
