FORCE GROMACS Plugin Changelog
==============================

Release 0.1.0
-------------

Released:

Release notes
~~~~~~~~~~~~~

Version 0.1.0 is the inital release of the ``force-bdss-plugin-gromacs`` package.

The following people contributed code changes for this release:

* Frank Longford
* Corran Webster

Features
~~~~~~~~
* BDSS plugin ``GromacsPlugin`` (#2), contributing with stand alone BDSS objects that can be
  used and customised 'out-of-the-box'
* Comes with pre-compiled Gromacs 2019-4 binaries (#23)
* Basic Gromacs python wrapper (#1, #2, #13, #14, #19, #28), with the ability to call Gromacs commands
  using the ``subprocess`` library, and chain several commands together using the ``GromacsPipeline``
  class.
* Reader and Writer classes (#1, #7, #12, #15, #30) for Gromacs coordinate, molecule and topology files
* Chemical objects module ``force_gromacs.chemicals`` (#27, #28, #30), containing generic hierarchical
  representations of chemical objects, such as particles, fragments and molecules.
* Simulation objects module ``force_gromacs.simulation_builders`` (#1, #2, #6, #27) containing base classes
  that can be used to construct and run a customised Gromacs MD simulation.
* Post-processing tools module ``force_gromacs.tools`` (#6, #9), containing useful routines to analyse
  MD simulation trajectories
* Three BDSS ``DataSource`` subclasses (#1, #2, #5, #6, #16, #27, #30): ``FragmentDataSource``,
  ``MoleculeDataSource`` and ``SimulationDataSource``
* One BDSS ``NotificationListener`` subclass (#2, #5, #22, #25): ``HPCWriter``