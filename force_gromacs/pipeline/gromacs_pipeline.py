from traits.api import (
    List, Tuple, Unicode, on_trait_change, Dict, Property
)

from force_gromacs.core.base_gromacs_process import BaseGromacsProcess
from force_gromacs.core.i_base_process import IBaseProcess


class GromacsPipeline(BaseGromacsProcess):
    """A simple pipeline for Gromacs commands, based on scikit-learn
    pipeline functionality that can sequentially apply a list of Gromacs
    commands using subprocess and retain the standard output/error."""

    # --------------------
    #  Regular Attributes
    # --------------------

    #: List of tuples (name, IBaseProcess) objects that are chained,
    #: in the order in which they are chained.
    steps = List(Tuple(Unicode, IBaseProcess))

    #: Output from the most recent Gromacs run
    run_output = Dict()

    # --------------------
    #      Properties
    # --------------------

    #: A dictionary representing `steps` with keys as the first element
    #: and values as the second element in each tuple
    named_steps = Property(Dict, depends_on='steps[]')

    # --------------------
    #      Defaults
    # --------------------

    def _run_output_default(self):
        return {name: {} for name, process in self.steps}

    # --------------------
    #      Listeners
    # --------------------

    def _get_named_steps(self):
        return dict(self.steps)

    @on_trait_change('dry_run,steps[]')
    def update_dry_run(self):
        """Syncs the dry_run attribute for each process in steps
        to the state of self.dry_run"""
        for name, process in self.steps:
            process.dry_run = self.dry_run

    # --------------------
    #  Protected Methods
    # --------------------

    def __len__(self):
        """
        Returns the length of the Pipeline
        """
        return len(self.steps)

    def __getitem__(self, ind):
        """Returns a sub-pipeline or a single command in the pipeline
        Indexing with an integer will return a command; using a slice
        returns another Pipeline instance which copies a slice of this
        Pipeline.
        """
        if isinstance(ind, slice):
            raise ValueError('Pipeline does not support slicing')
        try:
            name, process = self.steps[ind]
        except TypeError:
            # Not an int, try get step by name
            return self.named_steps[ind]
        return process

    def __iter__(self):
        """
        Generate (name, process) tuples from self.steps
        """
        for name, process in self.steps:
            yield name, process

    # --------------------
    #    Public Methods
    # --------------------

    def append(self, step):
        """Appends step to `self.steps` attribute"""
        self.steps.append(step)

    def bash_script(self):
        """Returns all terminal commands for steps

        Returns
        -------
        pipeline_commands : str
            Generated Gromacs commands as a string
        """
        bash_script = ''

        for name, process in self:
            bash_script += process.bash_script() + '\n'

        return bash_script

    def run(self):
        """Runs all terminal commands for steps and stores output
        from subprocess in `_run_output` """
        self.run_output = self._run_output_default()

        for name, process in self:
            returncode = process.run()

            self.run_output[name]['returncode'] = returncode
            self.run_output[name]['stderr'] = process.recall_stderr()
            self.run_output[name]['stdout'] = process.recall_stdout()
