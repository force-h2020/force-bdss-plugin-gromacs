from force_gromacs.simulation_builders.base_gromacs_simulation_builder import (
    BaseGromacsSimulationBuilder
)

from .pipelines import ProbeGromacsPipeline


class ProbeSimulationBuilder(BaseGromacsSimulationBuilder):

    def build_pipeline(self):
        return ProbeGromacsPipeline()

    def get_results_path(self):
        return '/path/to/trajectory.gro'
