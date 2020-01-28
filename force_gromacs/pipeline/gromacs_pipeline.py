from traits.api import (
    List, Tuple, Str
)

from force_gromacs.core.base_process import BaseProcess
from .base_pipeline import BasePipeline


class GromacsPipeline(BasePipeline):
    """A simple pipeline for Gromacs commands, based on scikit-learn
    pipeline functionality that can sequentially apply a list of Gromacs
    commands using subprocess and retain the standard output/error."""

    # --------------------
    #  Regular Attributes
    # --------------------

    #: List of tuples (name, BaseProcess) objects that are
    #: chained, in the order in which they are chained.
    steps = List(Tuple(Str, BaseProcess))
