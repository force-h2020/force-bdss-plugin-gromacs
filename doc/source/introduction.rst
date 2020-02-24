Introduction
============

GROMACS is a Molecular Dynamics (MD) package, primarily designed to simulate biomolecules,
such as proteins, lipids and nucleic acids.

A cross-platform distribution is available as an egg from EDM, currently
supporting version `2019.4 <http://manual.gromacs.org/documentation/2019-current/index.html>`_

Chemicals Module Design
~~~~~~~~~~~~~~~~~~~~~~~

The Force Gromacs wrapper is built on top of a small library defining a hierarchical
collection of generic chemical species, ``force_gromacs.chemicals``.
It is build for extensibility, providing base traits classes as well as the interfaces
for these objects that could be fulfilled by objects in an external package.

The lowest object in this hierarchy is the ``IParticle``, which defines a very simple
interface for a class that possesses both ``mass`` and ``charge`` attributes. A particle
is not therefore fixed to a specific length scale since a proton, atom, molecule or
large molecular complex species would all be able to fulfil this interface.

Next up from this is the ``IParticleGroup`` class, representing a collection of particles.
The interface inherits from ``IParticle``, so that a group of particles can also be
represented by a reduced representation given by a single particle.

In the atomistic length scale, we also introduce the ``IFragment`` class to describe
molecular fragments. A fragment represents a part of a molecule containing a single
or collection of covalently bonded particles. Therefore it inherits from ``IParticleGroup``,
but also contains the stoichiometric number of each fragment in the molecule.
For example, calcium cabonate :math:`CaCO_3` consists of 2 fragments,
the :math:`Ca^{2+}` atomic ion and the :math:`CO_3^{2-}` molecular ion:

.. math::
    CaCO_3 \leftrightarrow Ca^{2+} + CO_3^{2-}

Both species are free to dissociate, and therefore do not possess any constraints
in a MD simulation regarding their equations of motion. We can also freely add and take
away integer numbers of these objects in a simulation cell and calculate their molecular
concentrations in a mixture. However, in reality we cannot 'add' fragments from a jar
on the laboratory shelf, and instead describe formulations by their
constituent molecules (typically in concentration % by mass).

Therefore, the ``Molecule`` class is designed to represent a full computational
model for a chemical found in the laboratory. It contains a list of ``IFragment`` classes,
and must be overall electronically neutral. Some examples of how common molecules would
be represented in the '``IParticle`` : ``IFragment`` : ``Molecule``' model are provided below
(note: example partial charges are shown rather than ionic charges):

+-----------------------------+--------------------+---------------+
| ``IParticle``               |    ``IFragment``   |  ``Molecule`` |
+-----------------------------+--------------------+---------------+
|  :math:`Na^+, Cl^-`         | :math:`Na^+, Cl^-` | :math:`NaCl`  |
+-----------------------------+--------------------+---------------+
|  :math:`O^{2-},`            | :math:`H_2O`       | :math:`H_2O`  |
|  :math:`2 \times H^+`       |                    |               |
+-----------------------------+--------------------+---------------+
| :math:`Ca^{2+}, O^{2-},`    |                    |               |
| :math:`C, 2 \times O`       | :math:`Ca^{2+},`   |:math:`CaCO_2` |
|                             | :math:`CO_2^{2-}`  |               |
+-----------------------------+--------------------+---------------+