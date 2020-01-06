from traits.api import Instance, Unicode

from force_bdss.api import BaseDriverEvent


class SimulationProgressEvent(BaseDriverEvent):
    """ A DataSource class can emit this upon generation
    of a bash script to be passed into a HPCWriter.
    """
    #: The bash script for a Gromacs Experiment
    bash_script = Instance(Unicode)
