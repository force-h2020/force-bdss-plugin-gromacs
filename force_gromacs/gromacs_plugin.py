from force_bdss.api import BaseExtensionPlugin, plugin_id

from force_gromacs.data_sources.molecule.molecule_factory import (
    MoleculeFactory
)
from force_gromacs.notification_listeners.hpc_writer\
    .hpc_writer_factory import HPCWriterFactory


PLUGIN_VERSION = 0


class GromacsPlugin(BaseExtensionPlugin):
    """This plugin provides useful classes and DatsSource subclasses
    for creating and running Gromacs MD simulations.
    """

    id = plugin_id("force_gromacs", "plugin", PLUGIN_VERSION)

    def get_name(self):
        return "Gromacs Plugin"

    def get_description(self):
        return (
            "A plugin containing useful objects for running "
            "Gromacs simulations"
        )

    def get_version(self):
        return PLUGIN_VERSION

    #: Define the factory classes that you want to export to this list.
    def get_factory_classes(self):
        return [
            MoleculeFactory,
            HPCWriterFactory
        ]
