#!/usr/bin/env python
import argparse
import aiida
aiida.load_profile()
from aiida import orm
from aiida.engine import submit
from aiida.common.exceptions import NotExistent
from ase.io import read as aseread
from aiida_wannier90_theosworkflows.workflows import Wannier90BandsWorkChain

# Codenames for pw.x, pw2wannier90.x, projwfc.x and wannier90.x
# Please modify these according to your machine
str_pw = 'qe-6.5-pw@localhost'
str_pw2wan = 'qe-6.5-pw2wannier90@localhost'
str_projwfc = 'qe-6.5-projwfc@localhost'
str_wan = 'wannier90-3.1.0-wannier@localhost'


# Input dictionary for all the codes
codes = dict(
            pw_code = orm.Code.get_from_string(str_pw),
            pw2wannier90_code = orm.Code.get_from_string(str_pw2wan),
            projwfc_code = orm.Code.get_from_string(str_projwfc),
            wannier90_code = orm.Code.get_from_string(str_wan),
        )

def parse_arugments():
    '''
    Parser function for the protocol and xsf file.
    '''
    parser = argparse.ArgumentParser(
        description=
        "A launch script to run the AiiDA Wannier90BandsWorkChain for automated high-throughput Wannier functions."
    )
    parser.add_argument(
        "--xsf",
        "-x",
        help="Path to the input XSF structure file"
    )
    parser.add_argument(
        '-p',
        "--protocol",
        help=
        "Available protocols are 'theos-ht-1.0' and 'testing'",
        default="testing")
    args = parser.parse_args()
    return args

def read_structure(xsf_file):
    '''
    Read xsf file and convert into a stored StructureData
    '''
    structure = orm.StructureData(ase=aseread(xsf_file))
    structure.store()
    print('Structure {} read and stored with pk {}.'.format(
        structure.get_formula(), structure.pk))
    return structure

def add_to_group(node, group_name):
    '''
    Add node to a group, creates the group if necessary.
    '''
    if group_name is not None:
        try:
            g = orm.Group.get(label=group_name)
            group_statistics = "that already contains {} nodes".format(len(g.nodes))
        except NotExistent:
            g = orm.Group(label=group_name)
            group_statistics = "that does not exist yet"
            g.store()
        g.add_nodes(node)
        print("Wannier90BandsWorkChain<{}> will be added to the group {} {}".format(
            node.pk, group_name, group_statistics))

def print_help(workchain, structure):
    '''
    Print function to display useful information for the tutorial
    '''
    print('launched {} pk {} for structure {}'.format(
            workchain.process_type, workchain.pk, structure.get_formula()))
    print('')

    # print('#' * 72)
    # print('# INSTRUCTIONS ON HOW TO CONTINUE FROM HERE')
    # print('# AiiDA is now running the workflow.')
    # print(
    #     '# First of all, you can enter the AiiDA virtual environment typing:'
    # )
    # print('#    workon aiida')
    # print(
    #     '# You can monitor the state of the workflow with the following commands:'
    # )
    # print('# * Monitor the state of the workflow')
    # print('#     verdi process list -p1 -a')
    # print(
    #     '#   and check the status of the workflow with PK={}.'.format(
    #         wc_run.pk))
    print('# * Get a detailed state of the running workfow:')
    print('verdi process report {}'.format(workchain.pk))
        # print('#')
        # print(
        #     '# Once the workflow is finished, you can find the ID of the band'
        # )
        # print('# structure using the command:')
        # print('#     verdi node show {}'.format(wc_run.pk))
        # print(
        #     '# and then getting the value from the column PK for the row')
        # print(
        #     '# corresponding to the link label "MLWF_interpolated_bands".')
        # print('# ')
        # print('# With this PK, you can show the bands with xmgrace using')
        # print('# (replace <PK> with the PK you found in the step before):')
        # print('#   verdi data bands show -f xmgrace <PK>')
        # print('# or export to file using:')
        # print('#   verdi data bands export -f agr <PK>')
        # print('# ')
        # print('# If you want to compare also with the DFT band structure,')
        # print('# you can run the script')
        # print('#    ~/run_DFT_bands.py {}'.format(wc_run.pk))
        # print(
        #     '# (where {} is the PK of this Wannier90 workchain, passed in order'
        #     .format(wc_run.pk))
        # print('# to reuse its input structure and kpoints path.')
        # print('# Then, follow the instructions printed by that script.')
        # print('#' * 72)
        # print(
        #     '# Thanks for using the automated Wannier function workflows with AiiDA!'
        # )
        # print(
        #     '# Read instructions above to know how to check the results.')
        # print('#' * 72)
    # else:
    #     print('would launch {}'.format(structure.get_formula()))
    #print('Output will be added to group: {}'.format(g_name))

def submit_workchain(xsf_file, protocol):
    '''
    Wrapper to submit the Wannier90BandsWorkChain
    '''

    # Workchains can be grouped together into "groups"
    # Name of the group where the workchain will be added to
    group_name = 'scdm_workflow'
    
    # Check on the structure data type
    if isinstance(xsf_file, orm.StructureData):
        structure = xsf_file
    else:
        structure = read_structure(xsf_file)

    # Flags to control the workchain behaviour
    controls = {
        'retrieve_hamiltonian': orm.Bool(True),     # If True, retrieve Wannier Hamiltonian after the workflow has finished
        'only_valence': orm.Bool(False),            # If True, compute only valence bands (NB: use for insulators only!)
        'do_disentanglement': orm.Bool(False),      # If True, perform disentanglement procedure (minimise \Omega_I)
        'do_mlwf': orm.Bool(True),                  # If True, perform maximal-localisation (MLWF) procedure (minimise \tilde(\Omega))
    }

    # Prints informations
    if controls['only_valence']:
        print("Running only_valence/insulating, do_mlwf={} for {}".format(
            controls['do_mlwf'], structure.get_formula()))
    else:
        print("Running with conduction bands, do_disentanglement={}, do_mlwf={} for {}".
                format(controls['do_disentanglement'], controls['do_mlwf'], structure.get_formula()))

    wannier90_workchain_parameters = {
        "code": {
            'pw': codes['pw_code'],
            'pw2wannier90': codes['pw2wannier90_code'],
            'projwfc': codes['projwfc_code'],
            'wannier90': codes['wannier90_code']
        },
        "protocol": orm.Dict(dict={'name': protocol}),
        "structure": structure,
        "controls": controls
    }
    
    # Submits the workchain
    workchain = submit(Wannier90BandsWorkChain,
        **wannier90_workchain_parameters)
    
    # Adds workchain to a group
    add_to_group(workchain, group_name)

    # Prints help
    print_help(workchain, structure)
    return workchain.pk
   
if __name__ == "__main__":
    # Parsing input flags
    args = parse_arugments()
    # Submitting the Wannier90BandsWorkChain
    submit_workchain(args.xsf,args.protocol)
