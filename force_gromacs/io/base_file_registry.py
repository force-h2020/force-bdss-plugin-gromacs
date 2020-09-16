#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import os

from traits.api import HasStrictTraits, Dict, Str


class BaseFileRegistry(HasStrictTraits):
    """Helper class that can edit file names to possess
    a suitable format for different simulation software
    requirements"""

    #: Registry of extensions for each simulation file type
    extensions = Dict(Str, Str)

    def format_file_name(self, file_name, file_type):
        """Return formatted name depending on file type"""

        # Remove any existing file extensions that are recognised
        # by this class
        prefix, ext = os.path.splitext(file_name)
        if ext.strip('.') in self.extensions.values():
            file_name = prefix

        # Return desired format for extension
        return '.'.join([file_name, self.extensions[file_type]])
