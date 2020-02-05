from traits.api import Str, Property

from .file_registry import FileRegistry


class GromacsFileRegistry(FileRegistry):

    #: Prefix to each file name
    prefix = Str()

    #: Output coordinate file name
    coord_file = Property(Str, depends_on='prefix')

    #: Output binary file name
    binary_file = Property(Str, depends_on='prefix')

    #: Output topology file name
    top_file = Property(Str, depends_on='prefix')

    #: Output energy file name
    energy_file = Property(Str, depends_on='prefix')

    #: Output trajectory file name
    traj_file = Property(Str, depends_on='prefix')

    #: Output compressed trajectory file name
    comp_traj_file = Property(Str, depends_on='prefix')

    #: Output log file name
    log_file = Property(Str, depends_on='prefix')

    #: Output state file name
    state_file = Property(Str, depends_on='prefix')

    def _extensions_default(self):
        return {
            'coordinate': 'gro',
            'binary': 'tpr',
            'topology': 'top',
            'energy': 'edr',
            'log': 'log',
            'state': 'cpt',
            'compressed trajectory': 'xtc',
            'trajectory': 'trr',
            'molecule': 'itp',
            'index': 'ndx'
        }

    def _get_coord_file(self):
        return self.format_file_name(
            self.prefix + '_coord', 'coordinate')

    def _get_binary_file(self):
        return self.format_file_name(
            self.prefix + '_topol', 'binary')

    def _get_top_file(self):
        return self.format_file_name(
            self.prefix + '_topol', 'topology')

    def _get_energy_file(self):
        return self.format_file_name(
            self.prefix + '_ener', 'energy')

    def _get_traj_file(self):
        return self.format_file_name(
            self.prefix + '_traj', 'trajectory')

    def _get_comp_traj_file(self):
        return self.format_file_name(
            self.prefix + '_traj', 'compressed trajectory')

    def _get_log_file(self):
        return self.format_file_name(
            self.prefix + '_md', 'log')

    def _get_state_file(self):
        return self.format_file_name(
            self.prefix + '_state', 'state')
