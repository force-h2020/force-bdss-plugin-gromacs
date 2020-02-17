from force_gromacs.io.base_file_reader import BaseFileReader


class ProbeFileReader(BaseFileReader):

    def __ext_default(self):
        return 'file'

    def __comment_default(self):
        return '#'
