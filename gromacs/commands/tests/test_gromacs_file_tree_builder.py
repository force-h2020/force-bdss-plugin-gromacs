from unittest import TestCase, mock

from gromacs.commands.gromacs_file_tree_builder import (
    GromacsFileTreeBuilder
)

GROMACS_FILE_TREE_MKPATH = (
    "gromacs.commands.gromacs_file_tree_builder.os.mkdir"
)


def mock_empty(value):
    return None


class TestGromacsFileTreeBuilder(TestCase):

    def setUp(self):

        self.builder = GromacsFileTreeBuilder(
            directory='test_experiment_1',
            folders=[
                '1_build', '2_minimize', '3_production'
            ],
            dry_run=True
        )

    def test__make_directory(self):
        with mock.patch(GROMACS_FILE_TREE_MKPATH) as mock_mkdir:
            mock_mkdir.side_effect = mock_empty
            self.builder._make_directory('')
            mock_mkdir.assert_not_called()

        self.builder.dry_run = False
        with mock.patch(GROMACS_FILE_TREE_MKPATH) as mock_mkdir:
            mock_mkdir.side_effect = mock_empty
            self.builder._make_directory('')
            mock_mkdir.assert_called()

    def test__create_directories(self):
        directory_list = self.builder._create_directories()

        self.assertEqual(4, len(directory_list))
        self.assertEqual(
            'test_experiment_1', directory_list[0]
        )
        self.assertEqual(
            'test_experiment_1/1_build', directory_list[1]
        )
        self.assertEqual(
            'test_experiment_1/2_minimize', directory_list[2]
        )
        self.assertEqual(
            'test_experiment_1/3_production', directory_list[3]
        )

    def test_bash_script(self):

        res = self.builder.bash_script()

        res = res.split('\n')
        self.assertEqual(4, len(res))
        self.assertEqual(
            'mkdir test_experiment_1', res[0]
        )
        self.assertEqual(
            'mkdir test_experiment_1/1_build', res[1]
        )
        self.assertEqual(
            'mkdir test_experiment_1/2_minimize', res[2]
        )
        self.assertEqual(
            'mkdir test_experiment_1/3_production', res[3]
        )

    def test_run(self):
        with mock.patch(GROMACS_FILE_TREE_MKPATH) as mock_mkdir:
            mock_mkdir.side_effect = mock_empty
            self.builder.run()
            mock_mkdir.assert_not_called()

        self.builder.dry_run = False
        with mock.patch(GROMACS_FILE_TREE_MKPATH) as mock_mkdir:
            mock_mkdir.side_effect = mock_empty
            self.builder.run()
            self.assertEqual(4, mock_mkdir.call_count)
