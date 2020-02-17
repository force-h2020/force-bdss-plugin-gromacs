from unittest import TestCase

from force_gromacs.chemicals.base_particle_group import BaseParticleGroup
from force_gromacs.tests.probe_classes.chemicals import ProbeParticle


class TestBaseParticleGroup(TestCase):

    def setUp(self):

        self.group = BaseParticleGroup()

    def test__init__(self):

        self.assertEqual([], self.group.particles)
        self.assertEqual([], self.group.bonds)
        self.assertEqual(0, self.group.mass)
        self.assertEqual(0, self.group.charge)

    def test_mass_charge(self):

        self.group.particles.append(
            ProbeParticle(mass=10, charge=-1))

        self.assertEqual(10, self.group.mass)
        self.assertEqual(-1, self.group.charge)

        self.group.particles.append(
            ProbeParticle(mass=10, charge=1))

        self.assertEqual(20, self.group.mass)
        self.assertEqual(0, self.group.charge)
