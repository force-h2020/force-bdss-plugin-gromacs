from traits.api import (
    HasStrictTraits, List, Tuple, Str, on_trait_change,
    Dict, Property, provides, Bool
)

from force_gromacs.core.i_process import IProcess


@provides(IProcess)
class BasePipeline(HasStrictTraits):
    """A simple pipeline for subprocess commands, based on scikit-learn
    pipeline functionality that can sequentially apply a list of bash
    commands using subprocess and retain the standard output/error."""

    # --------------------
    #  Regular Attributes
    # --------------------

    #: List of tuples (name, IProcess) objects that are chained,
    #: in the order in which they are chained.
    steps = List(Tuple(Str, IProcess))

    #: Output from the most recent pipeline run
    run_output = Dict()

    #: Whether or not to perform a 'dry run' i.e. build the
    #: command but do not call subprocess to run it
    dry_run = Bool()

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

    def recall_stderr(self):
        """Returns all stderr messages as a dictionary"""
        return {name: process.recall_stderr()
                for name, process in self.steps}

    def recall_stdout(self):
        """Returns all stdout messages as a dictionary"""
        return {name: process.recall_stdout()
                for name, process in self.steps}

    def bash_script(self):
        """Returns all terminal commands for steps

        Returns
        -------
        pipeline_commands : str
            Generated bash commands as a string
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
