#!/usr/bin/env runaiida
import aiida
aiida.load_profile()
import argparse
from aiida import orm
from aiida.engine import submit, run_get_node
from aiida.common.exceptions import NotExistent
from ase.io import read as aseread
from w90_auto_dos.bands import Wannier90BandsWorkChain

#Flags to control the workflow
do_disentanglement = False
do_mlwf = True
plot_wannier_functions = False
retrieve_hamiltonian = True
group_name = 'autowannier_oxford_tutorial_2020'

#codenames
str_pw = 'qe-6.5-pw@localhost'
str_pw2wan = 'qe-6.5-pw2wannier90@localhost'
str_projwfc = 'qe-6.5-projwfc@localhost'
str_wan = 'wannier90@localhost'

def update_group_name(in_group_name, only_valence, do_disen, do_mlwf, exclude_bands=None):
    group_name = in_group_name
    if only_valence:
        group_name += "_onlyvalence"
    else:
        group_name += "_withconduction"
    if do_disen:
        group_name += '_disentangle'
    if do_mlwf:
        group_name += '_mlwf'
    if exclude_bands is not None:
        group_name += '_excluded{}'.format(len(exclude_bands))
    # group_name += '_' + str(kp_density_nscf)
    return group_name
    
def read_structure(xsf_file):
    structure = orm.StructureData(ase=aseread(xsf_file))
    structure.store()
    print('Structure {} read and stored with pk {}.'.format(
        structure.get_formula(), structure.pk))
    return structure

def add_to_group(node, group_name):
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
def parse_arugments():
    import argparse
    parser = argparse.ArgumentParser(
        description=
        "A script to run the AiiDA workflows to automatically compute the MLWF using the SCDM method and the automated protocol described in the Vitale et al. paper"
    )
    parser.add_argument(
        "--xsf",
        metavar="XSF_FILENAME",
        help="path to an input XSF file, that you can find in the folder ~/xsf"
    )
    parser.add_argument(
        '-v',
        "--only-valence",
        help=
        "Compute only for valence bands (you must be careful to apply this only for insulators!)",
        action="store_true")
    parser.add_argument(
        '-s',
        '--kpoints-scf',
        type=float,
        help=
        "density of kpoints for the SCF step (units: 1/angstrom, default=0.2)",
        default=0.2)
    parser.add_argument(
        '-n',
        '--kpoints-nscf',
        type=float,
        help=
        "density of kpoints for the NSCF step (units: 1/angstrom, default=0.2)",
        default=0.2)
    parser.add_argument(
        '-p',
        '--protocol',
        type=str,
        help=
        "protocol for the DFT calculations (default='theos-ht-1.0')",
        default='theos-ht-1.0')
   
     
    args = parser.parse_args()

    return args

def submit_workchain(xsf_file, group_name, only_valence, do_disentanglement, do_mlwf, protocol):

    group_name = update_group_name(
       group_name, only_valence, do_disentanglement, do_mlwf)

    structure = read_structure(xsf_file)
    controls = {
        'retrieve_hamiltonian': orm.Bool(retrieve_hamiltonian),
        'only_valence': orm.Bool(only_valence)
    }

    if only_valence:
        print("Running 'only_valence/insulating', do_mlwf={} for {}".format(
            do_mlwf, structure.get_formula()))
    else:
        print("Running 'with conduction bands', do_disentanglement={}, do_mlwf={} for {}".
                format(do_disentanglement, do_mlwf, structure.get_formula()))

    pw_code = orm.Code.get_from_string(str_pw)
    pw2wannier90_code = orm.Code.get_from_string(str_pw2wan)
    projwfc_code = orm.Code.get_from_string(str_projwfc)
    wannier90_code = orm.Code.get_from_string(str_wan)

    _, workchain = run_get_node(Wannier90BandsWorkChain,
        code={
            'pw': pw_code,
            'pw2wannier90': pw2wannier90_code,
            'projwfc': projwfc_code,
            'wannier90': wannier90_code
        },
        protocol=orm.Dict(dict={'name': protocol}),
        structure=structure,
        controls=controls
    )

    add_to_group(workchain, group_name)


if __name__ == "__main__":
    
    #parse the input
    args = parse_arugments()
    xsf_file = args.xsf
    xsf_file = './xsf/' + xsf_file
    only_valence = args.only_valence
    kp_density_scf = args.kpoints_scf
    kp_density_nscf = args.kpoints_nscf
    protocol = args.protocol

    #submit the workhain
    submit_workchain(
        xsf_file,
        group_name,
        only_valence,
        do_disentanglement,
        do_mlwf,
        protocol
    )
