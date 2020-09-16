#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import os


path = os.path.dirname(__file__)

gromacs_coordinate_file = os.path.join(
    path, 'example_gromacs_coordinate_file.gro')
gromacs_topology_file = os.path.join(
    path, 'example_gromacs_topology_file.top')
gromacs_molecule_file = os.path.join(
    path, 'example_gromacs_molecule_file.itp')
lammps_data_file = os.path.join(
    path, 'example_lammps_data_file.data')
