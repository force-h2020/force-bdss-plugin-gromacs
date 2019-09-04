from traits.api import Instance

from force_bdss.api import BaseDriverEvent, DataValue
from force_bdss.io.workflow_writer import pop_dunder_recursive


class SimulationProgressEvent(BaseDriverEvent):
    """ A DataSource class can emit this upon generation
    of a bash script to be passed into a HPCWriter.
    """
    #: The bash script for a Gromacs Experiment
    bash_script = Instance(DataValue)

    def __getstate__(self):
        d = pop_dunder_recursive(super().__getstate__())
        d["bash_script"] = d["bash_script"].__getstate__()
        return d
