from unittest import TestCase, mock

from force_gromacs.io.base_file_reader import BaseFileReader
from force_gromacs.tests.probe_classes.io import (
    ProbeFileReader
)
from force_gromacs.tests.dummy_classes import dummy_function

FILE_READER_OPEN_PATH = (
    "force_gromacs.io.base_file_reader.open"
)
CHECK_FILE_TYPES_PATH = (
    "force_gromacs.io.base_file_reader.BaseFileReader._check_file_types"
)

top_file = """# This is a comment
              #
              This line is fine
              #
              This line # should end here"""


class TestBaseFileReader(TestCase):

    def setUp(self):

        self.reader = ProbeFileReader()

    def test_not_implemented(self):

        reader = BaseFileReader()

        with self.assertRaises(NotImplementedError):
            self.assertIsNone(reader._ext)

        with self.assertRaises(NotImplementedError):
            self.assertIsNone(reader._comment)

    def test__read_file(self):

        mock_open = mock.mock_open()

        with mock.patch(FILE_READER_OPEN_PATH, mock_open,
                        create=True),\
                mock.patch(CHECK_FILE_TYPES_PATH) as mock_check:
            mock_check.side_effect = dummy_function
            self.reader._read_file(
                'some_path'
            )
            mock_open.assert_called()

    def test__remove_comments(self):
        top_lines = top_file.split('\n')

        cleaned_lines = self.reader._remove_comments(top_lines)

        self.assertEqual(2, len(cleaned_lines))
        self.assertEqual('This line is fine', cleaned_lines[0])
        self.assertEqual('This line # should end here', cleaned_lines[1])

    def test__get_data(self):

        with self.assertRaises(NotImplementedError):
            self.reader._get_data(None)

    def test_read(self):

        with self.assertRaises(NotImplementedError):
            self.reader.read(None)
