from force_bdss.api import BaseDataSourceFactory

from .molecule_model import MoleculeDataSourceModel
from .molecule_data_source import MoleculeDataSource


class MoleculeFactory(BaseDataSourceFactory):

    def get_identifier(self):
        return "molecule"

    def get_name(self):
        return "Gromacs Molecule"

    def get_model_class(self):
        return MoleculeDataSourceModel

    def get_data_source_class(self):
        return MoleculeDataSource
