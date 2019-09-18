import logging

import numpy as np

from .base_file_reader import BaseFileReader

log = logging.getLogger(__name__)


class GromacsCoordinateReader(BaseFileReader):
    """Class parses Gromacs coordinate .gro file and returns
    data required for each molecular type.
    """

    # ------------------
    #     Defaults
    # ------------------

    def __ext_default(self):
        """Default extension for this reader subclass"""
        return 'gro'

    # ------------------
    #  Private Methods
    # ------------------

    def _get_data(self, file_lines, n_frames=None):
        """Process data from a parsed Gromacs file"""

        header = file_lines[0]
        n_particles = int(file_lines[1].strip())
        n_lines = n_particles + 3

        if n_frames is None:
            n_frames = len(file_lines) // n_lines

        mol_ref = []
        atom_ref = []
        dimensions = np.zeros((n_frames, 3))
        coordinates = np.zeros((n_frames, n_particles, 3))

        for frame in range(n_frames):
            start = frame * n_lines + 2
            end = (frame + 1) * n_lines

            for index, line in enumerate(file_lines[start: end]):

                line = line.split()

                if index == n_particles:
                    coord = np.array([float(line[0]),
                                      float(line[1]),
                                      float(line[2])])
                    dimensions[frame] = coord


                else:
                    if frame == 0:
                        mol_ref.append(line[0])
                        atom_ref.append(line[1])

                    coord = np.array([float(line[3]),
                                      float(line[4]),
                                      float(line[5])])

                    coordinates[frame, index] = coord

        return mol_ref, atom_ref, coordinates, dimensions

    # ------------------
    #   Public Methods
    # ------------------

    def read(self, file_path, n_frames=None):
        """ Open Gromacs coordinate file located at `file_path` and return
         processed data

        Parameters
        ----------
        file_path: str
            File path of Gromacs coordinate file
        n_frames: int, optional
            Maximum number of frames to read

        Returns
        -------
        data : dict
            Dictionary containing data (including molecule and atom
            references, and atomic coordinates) extracted from Gromacs
            coordinate file. Keys refer to the symbol of each
            molecular species.
        """

        try:
            file_lines = self._read_file(file_path)
        except IOError as e:
            log.exception('unable to open "{}"'.format(file_path))
            raise e

        try:
            (mol_ref, atom_ref,
             coordinates, dimensions) = self._get_data(file_lines, n_frames)
        except (IndexError, IOError) as e:
            log.exception('unable to load data from "{}"'.format(file_path))
            raise e

        data = {
            'mol_ref': mol_ref,
            'atom_ref': atom_ref,
            'coord': coordinates,
            'dim': dimensions,
        }

        return data
