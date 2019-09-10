from force_bdss.api import BaseDataSourceFactory

from .simulation_model import SimulationDataSourceModel
from .simulation_data_source import SimulationDataSource


class SimulationFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "simulation"

    def get_name(self):
        return "Gromacs Simulation"

    def get_model_class(self):
        return SimulationDataSourceModel

    def get_data_source_class(self):
        return SimulationDataSource
