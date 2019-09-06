from force_bdss.api import BaseDataSourceFactory

from .fragment_model import FragmentDataSourceModel
from .fragment_data_source import FragmentDataSource


class FragmentFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "fragment"

    def get_name(self):
        return "Gromacs Molecular Fragment"

    def get_model_class(self):
        return FragmentDataSourceModel

    def get_data_source_class(self):
        return FragmentDataSource
