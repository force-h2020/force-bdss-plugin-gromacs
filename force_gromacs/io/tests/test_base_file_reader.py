from unittest import TestCase, mock

from force_gromacs.io.base_file_reader import (
    BaseFileReader
)
from force_gromacs.tests.dummy_classes import dummy_function

FILE_READER_OPEN_PATH = (
    "force_gromacs.io.base_file_reader.open"
)
CHECK_FILE_TYPES_PATH = (
    "force_gromacs.io.base_file_reader.BaseFileReader._check_file_types"
)


class TestBaseFileReader(TestCase):

    def setUp(self):

        self.reader = BaseFileReader()

    def test___init__(self):

        with self.assertRaises(NotImplementedError):
            self.assertIsNone(self.reader._ext)

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

    def test__get_data(self):

        with self.assertRaises(NotImplementedError):
            self.reader._get_data(None)

    def test_read(self):

        with self.assertRaises(NotImplementedError):
            self.reader.read(None)
