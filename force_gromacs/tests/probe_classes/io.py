#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_gromacs.io.base_file_reader import BaseFileReader


class ProbeFileReader(BaseFileReader):

    def __ext_default(self):
        return 'file'

    def __comment_default(self):
        return '#'
