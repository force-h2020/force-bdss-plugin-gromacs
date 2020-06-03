#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from traits.trait_errors import TraitError

from force_gromacs.commands.gromacs_commands import (
    Gromacs_genbox, Gromacs_grompp, Gromacs_genion,
    Gromacs_mdrun, Gromacs_genconf, Gromacs_trjconv,
    Gromacs_select, Gromacs_solvate, Gromacs_insert_molecules
)


class TestGromacsCommands(TestCase):

    def setUp(self):
        #: Create Gromacs command objects
        self.genconf = Gromacs_genconf(dry_run=False)
        self.genbox = Gromacs_genbox(dry_run=False)
        self.solvate = Gromacs_solvate(dry_run=False)
        self.insert_molecules = Gromacs_insert_molecules(dry_run=False)
        self.grompp = Gromacs_grompp(dry_run=False)
        self.genion = Gromacs_genion(dry_run=False)
        self.mdrun = Gromacs_mdrun(dry_run=False)
        self.mdrun_mpi = Gromacs_mdrun(mpi_run=True, dry_run=False)
        self.select = Gromacs_select(dry_run=False)
        self.trjconv = Gromacs_trjconv(dry_run=False)

    def test_readonly(self):
        with self.assertRaises(TraitError):
            self.genbox.name = ''

        with self.assertRaises(TraitError):
            self.genbox.flags = []

    def test_genconf(self):

        input_options = {
            '-f': 'test_coord.gro',
            '-o': 'test_output.gro',
            '-nbox': 30
        }

        self.genconf.command_options = input_options
        command = self.genconf.bash_script()
        self.assertIn('genconf', command)
        self.assertIn(' -f test_coord.gro', command)
        self.assertIn(' -o test_output.gro', command)
        self.assertIn(' -nbox 30', command)

        self.genconf.command_options = {
            '-h': True}
        self.assertEqual(0, self.genconf.run())
        self.assertIn('SYNOPSIS', self.genconf.recall_stdout())

    def test_genbox(self):

        input_options = {
            '-cp': 'test_coord.gro',
            '-nmol': 30,
            '-not_a_flag': 60,
            '-o': 'test_output.gro',
            '-try': True}

        self.genbox.command_options = input_options
        command = self.genbox.bash_script()
        self.assertNotIn('gmx', command)
        self.assertIn('genbox', command)
        self.assertIn(' -cp test_coord.gro', command)
        self.assertIn(' -o test_output.gro', command)
        self.assertIn(' -try', command)
        self.assertIn(' -nmol 30', command)
        self.assertNotIn(' -not_a_flag 60', command)

    def test_solvate(self):

        input_options = {
            '-cp': 'test_coord.gro',
            '-p': 'test_top.top',
            '-not_a_flag': 60,
            '-o': 'test_output.gro',
            '-vel': True}

        self.solvate.command_options = input_options
        command = self.solvate.bash_script()
        self.assertIn('solvate', command)
        self.assertIn(' -cp test_coord.gro', command)
        self.assertIn(' -p test_top.top', command)
        self.assertIn(' -o test_output.gro', command)
        self.assertIn(' -vel', command)
        self.assertNotIn(' -not_a_flag 60', command)

        self.genconf.command_options = {
            '-h': True}
        self.assertEqual(0, self.genconf.run())
        self.assertIn('SYNOPSIS', self.genconf.recall_stdout())

    def test_insert_molecules(self):

        input_options = {
            '-cp': 'test_coord.gro',
            '-nmol': 30,
            '-not_a_flag': 60,
            '-o': 'test_output.gro',
            '-try': True}

        self.insert_molecules.command_options = input_options
        command = self.insert_molecules.bash_script()
        self.assertIn('insert-molecules', command)
        self.assertNotIn(' -cp test_coord.gro', command)
        self.assertIn(' -o test_output.gro', command)
        self.assertIn(' -try', command)
        self.assertIn(' -nmol 30', command)
        self.assertNotIn(' -not_a_flag 60', command)

        self.insert_molecules.command_options = {
            '-h': True}
        self.assertEqual(0, self.insert_molecules.run())
        self.assertIn('SYNOPSIS',
                      self.insert_molecules.recall_stdout())

    def test_grompp(self):

        input_options = {
            '-f': 'test_parm.mdp',
            '-p': 'test_top.top',
            '-c': 'test_coord.gro',
            '-o': 'test_top.trp',
            '-maxwarn': 4,
            'ci': 'nonsense'}
        self.grompp.command_options = input_options
        command = self.grompp.bash_script()
        self.assertIn('grompp', command)
        self.assertIn(' -f test_parm.mdp', command)
        self.assertIn(' -o test_top.trp', command)
        self.assertIn(' -c test_coord.gro', command)
        self.assertIn(' -p test_top.top', command)
        self.assertIn(' -maxwarn 4', command)
        self.assertNotIn(' ci nonsense', command)

        self.grompp.command_options = {
            '-h': True}
        self.assertEqual(0, self.grompp.run())
        self.assertIn('SYNOPSIS',
                      self.grompp.recall_stdout())

    def test_genion(self):

        input_options = {
            '-s': 'test_top.trp',
            '-p': 'test_top.top',
            '-o': 'test_coord_1.gro',
            '-pname': 'test_coord_2.gro',
            '-np': 64,
            '-pq': 1,
            '-cp': 'problem'}
        self.genion.command_options = input_options
        command = self.genion.bash_script()
        self.assertIn('genion', command)
        self.assertIn(' -s test_top.trp ', command)
        self.assertIn(' -o test_coord_1.gro', command)
        self.assertIn(' -np 64', command)
        self.assertIn(' -p test_top.top', command)
        self.assertIn(' -pname test_coord_2.gro', command)
        self.assertIn(' -pq 1', command)
        self.assertNotIn(' -cp problem', command)

        self.genion.command_options = {
            '-h': True}
        self.assertEqual(0, self.genion.run())
        self.assertIn('SYNOPSIS',
                      self.genion.recall_stdout())

        self.genion.user_input = 'W'
        command = self.genion.bash_script()
        self.assertIn("echo 'W' | gmx genion", command)

    def test_mdrun(self):

        input_options = {
            '-s': 'test_top.trp',
            '-e': 'test_ener.edr',
            '-o': 'test_traj.trr',
            '-x': 'test_traj.xtc',
            '-c': 'test_coord.gro',
            '-g': 'test_md.log'}

        self.mdrun.command_options = input_options
        command = self.mdrun.bash_script()
        self.assertIn('mdrun', command)
        self.assertIn(' -s test_top.trp ', command)
        self.assertIn(' -o test_traj.trr', command)
        self.assertIn(' -g test_md.log', command)
        self.assertIn(' -e test_ener.edr', command)
        self.assertIn(' -x test_traj.xtc', command)
        self.assertIn(' -c test_coord.gro', command)

        self.mdrun.command_options = {
            '-h': True}
        self.assertEqual(0, self.mdrun.run())
        self.assertIn('SYNOPSIS',
                      self.mdrun.recall_stdout())

        self.mdrun_mpi.command_options = input_options
        command = self.mdrun_mpi.bash_script()
        self.assertIn('mpirun -np 1', command)
        self.assertIn('mdrun', command)

        self.mdrun_mpi.executable = ''
        command = self.mdrun_mpi.bash_script()
        self.assertIn('mdrun_mpi', command)

    def test_trjconv(self):
        command_options = {
            '-f': 'test_traj.xtc',
            '-s': 'test_coord.gro',
            '-pbc': 'nojump'
        }

        self.trjconv.command_options = command_options
        command = self.trjconv.bash_script()
        self.assertIn('trjconv', command)
        self.assertIn(' -f test_traj.xtc ', command)
        self.assertIn(' -s test_coord.gro', command)
        self.assertIn(' -pbc nojump', command)

        self.trjconv.command_options = {
            '-h': True}
        self.assertEqual(0, self.trjconv.run())
        self.assertIn('SYNOPSIS',
                      self.trjconv.recall_stdout())

    def test_select(self):

        command_options = {
            '-f': 'test_traj.xtc',
            '-on': 'test_index.ntx',
            '-select': '"( resname W )"'
        }

        self.select.command_options = command_options
        command = self.select.bash_script()
        self.assertIn('select', command)
        self.assertIn(' -f test_traj.xtc ', command)
        self.assertIn(' -on test_index.ntx', command)
        self.assertIn(' -select "( resname W )"', command)

        self.select.command_options = {
            '-h': True}
        self.assertEqual(0, self.select.run())
        self.assertIn('SYNOPSIS',
                      self.select.recall_stdout())

        self.select.executable = ''
        command = self.select.bash_script()
        self.assertIn('g_select', command)
