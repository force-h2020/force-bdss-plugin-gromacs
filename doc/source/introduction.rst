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
large molecular complex species would all be able to fulfil this interface. An example of
an object that fulfils this interface is the ``GromacsParticle`` class.

.. code-block:: python

    >>> my_particle = GromacsParticle(mass=12, charge=0)
    >>> my_particle.mass
    12.0
    >>> my_particle.charge
    0.0

Next up from this is the ``IParticleGroup`` class, representing a collection of particles.
The interface inherits from ``IParticle``, so that a group of particles can also be
represented by a reduced representation given by a single particle.

In the atomistic length scale, we also introduce the ``IFragment`` class to describe
molecular fragments. A fragment represents a part of a molecule containing a single
or collection of covalently bonded particles. Therefore it inherits from ``IParticleGroup``,
but also contains the attribute ``stoichiometry``, the stoichiometric number of each
fragment in the molecule. An example of an object that fulfils this interface is the
``GromacsFragment`` class, which also contains (optional) information regarding the geometry
of molecular fragments.

.. code-block:: python

    >>> my_fragment = GromacsFragment(particles=[my_particle])
    >>> my_fragment.mass
    12.0
    >>> my_fragment.charge
    0.0
    >>> my_fragment.stoichiometry
    1

A molecule of sodium cabonate :math:`Na_2CO_3` consists of 3 fragments:
two :math:`Na^{+}` atomic ions and the :math:`CO_3^{2-}` molecular ion:

.. math::
    Na_2CO_3 \leftrightarrow 2Na^{+} + CO_3^{2-}

All ionic species are free to dissociate, and therefore do not possess any constraints
in a MD simulation regarding their equations of motion. We can also freely add and take
away integer numbers of these objects in a simulation cell and calculate their molecular
concentrations in a mixture. However, in reality we cannot 'add' fragments from a jar
on the laboratory shelf, and instead describe formulations by their
constituent molecules (typically in concentration % by mass).

Therefore, the ``Molecule`` class is designed to represent a full computational
model for a chemical found in the laboratory. It contains a list of ``IFragment`` classes,
and must be overall electronically neutral. We can describe the calcium carbonate molecule
by the following ``force_gromacs`` objects:

Firstly the constituent atomic particles:

.. code-block:: python

    >>> sodium = GromacsParticle(element='Na', mass=11, charge=1)
    >>> carbon = GromacsParticle(element='C', mass=12, charge=4)
    >>> oxygen = GromacsParticle(element='O', mass=16, charge=-2)

Next the fragment ions:

.. code-block:: python

    >>> sodium_ions = GromacsFragment(particles=[sodium], stoichiometry=2)
    >>> sodium_ions.mass
    22.0
    >>> sodium_ions.charge
    2.0

    >>> carbonate_ion = GromacsFragment(particles=[carbon] + 3 * [oxygen])
    >>> carbonate_ion.mass
    60.0
    >>> carbonate_ion.charge
    -2.0

And finally the full molecule:

.. code-block:: python

    >>> sodium_carbonate = Molecule(fragments=[sodium_ions, carbonate_ion])
    >>> sodium_carbonate.mass
    82.0
    >>> sodium_carbonate.charge
    0.0
    >>> sodium_carbonate.neutral
    True
