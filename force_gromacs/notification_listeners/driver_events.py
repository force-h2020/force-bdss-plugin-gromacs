#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Str

from force_bdss.api import BaseDriverEvent


class SimulationProgressEvent(BaseDriverEvent):
    """ A DataSource class can emit this upon generation
    of a bash script to be passed into a HPCWriter.
    """
    #: The bash script for a Simulation Experiment
    bash_script = Str()
