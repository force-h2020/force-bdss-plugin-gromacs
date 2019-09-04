from itertools import islice

from traits.api import (
    List, Tuple, Unicode, on_trait_change, Dict
)

from force_gromacs.core.base_gromacs_process import BaseGromacsProcess


class GromacsPipeline(BaseGromacsProcess):
    """ A simple pipeline for Gromacs commands, based on scikit-learn
    pipeline functionality that can sequentially apply a list of Gromacs
    commands using subprocess and retain the standard output/error."""

    #: List of tuples (name, BaseGromacsProcess) objects that are chained,
    #: in the order, in which they are chained.
    steps = List(Tuple(Unicode, BaseGromacsProcess))

    #: Output from the most recent Gromacs run
    run_output = Dict()

    @on_trait_change('dry_run,steps[]')
    def update_dry_run(self):
        for name, process in self.steps:
            process.dry_run = self.dry_run

    def _iter(self):
        """
        Generate (idx, (name, command)) tuples from self.steps
        """
        stop = len(self.steps)
        generator = enumerate(islice(self.steps, 0, stop))

        for idx, (name, command) in generator:
            yield idx, name, command

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
            if ind.step not in (1, None):
                raise ValueError('Pipeline slicing only supports a step of 1')
            return self.__class__(self.steps[ind])
        try:
            name, command = self.steps[ind]
        except TypeError:
            # Not an int, try get step by name
            return self.named_steps[ind]
        return command

    @property
    def named_steps(self):
        return dict(**dict(self.steps))

    def append(self, step):
        """Appends step to `self.steps` attribute after type checking"""
        self.steps.append(step)

    def bash_script(self):
        """Returns all terminal commands for steps

        Returns
        -------
        pipeline_commands : str
            Generated Gromacs commands as a string
        """
        bash_script = ''

        for (step_idx,
             name,
             command) in self._iter():

            bash_script += command.bash_script() + '\n'

        return bash_script

    def run(self):
        """Runs all terminal commands for steps and stores output
        from subprocess in `_run_output` """
        self.run_output = {name: {} for name, command in self.steps}

        for (step_idx,
             name,
             command) in self._iter():

            returncode = command.run()

            self.run_output[name]['returncode'] = returncode
            self.run_output[name]['stderr'] = command.recall_stderr()
            self.run_output[name]['stdout'] = command.recall_stdout()
