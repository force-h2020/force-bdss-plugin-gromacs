from unittest import TestCase

from force_gromacs.io.file_registry import FileRegistry


class TestFileRegistry(TestCase):

    def setUp(self):

        self.file_registry = FileRegistry(
            extensions={'coordinate': 'gro'}
        )

    def test_format_file_name(self):

        file_name = '/path/to/some/file_prefix'
        self.assertEqual(
            '/path/to/some/file_prefix.gro',
            self.file_registry.format_file_name(file_name, 'coordinate')
        )

        file_name = '/path/to/some/file_prefix_w_extension.ext'
        self.assertEqual(
            '/path/to/some/file_prefix_w_extension.gro',
            self.file_registry.format_file_name(file_name, 'coordinate')
        )

        file_name = '/path/to/some/.hidden_file_prefix'
        self.assertEqual(
            '/path/to/some/.hidden_file_prefix.gro',
            self.file_registry.format_file_name(file_name, 'coordinate')
        )
