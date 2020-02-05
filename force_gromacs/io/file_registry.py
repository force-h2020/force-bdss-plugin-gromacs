import os

from traits.api import HasStrictTraits, Dict, Str


class FileRegistry(HasStrictTraits):

    #: Registry of extensions for each simulation file type
    extensions = Dict(Str, Str)

    def format_file_name(self, file_name, file_type):
        """Return formatted name depending on file type"""

        # Remove any existing file extensions that are recognised
        # by this FileRegisty
        prefix, ext = os.path.splitext(file_name)
        if ext.strip('.') in self.extensions.values():
            file_name = prefix

        # Return desired format for extension
        return '.'.join([file_name, self.extensions[file_type]])
