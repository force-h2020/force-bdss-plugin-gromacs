from force_gromacs.pipelines.base_pipeline import BasePipeline


class GromacsPipeline(BasePipeline):
    """A simple pipeline for Gromacs commands, based on scikit-learn
    pipeline functionality that can sequentially apply a list of Gromacs
    commands using subprocess and retain the standard output/error."""
    pass
