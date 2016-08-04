import mockfs
import unittest

from kubernetes_downward_api import parse


class TestKubernetesDownwardAPI(unittest.TestCase):
    def setUp(self):
        super(TestKubernetesDownwardAPI, self).setUp()
        self.mockfs = mockfs.replace_builtins()

        self.addCleanup(mockfs.restore_builtins)

    def test_parse_returns_raw_file_as_value(self):
        self.mockfs.add_entries({
            '/basic/file': 'value'
        })

        self.assertEqual({
            'file': 'value'
        }, parse(['/basic/file']))

    def test_parse_returns_complex_file_as_fields(self):
        self.mockfs.add_entries({
            '/complex/file': '''\
key1="value1"
key2="value2"
'''
        })

        self.assertEqual({
            'file': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }, parse(['/complex/file']))

    def test_parse_ignores_blank_lines(self):
        self.mockfs.add_entries({
            '/complex/file': '\n' + '    \n' + 'key1="value1"\n' + ' \n' + 'key2="value2"\n'
        })

        self.assertEqual({
            'file': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }, parse(['/complex/file']))

    def test_parse_raises_if_complex_file_has_line_without_key_value_pair(self):
        self.mockfs.add_entries({
            '/complex/file': 'key1="value1"\n' + 'something\n'
        })

        with self.assertRaises(ValueError):
            parse(['/complex/file'])

    def test_parse_parses_all_files_in_directory(self):
        self.mockfs.add_entries({
            '/dir/file': 'value',
            '/dir/other': 'content'
        })

        self.assertEqual({
            'file': 'value',
            'other': 'content'
        }, parse(['/dir']))

    def test_parse_skips_hidden_files_in_directory(self):
        self.mockfs.add_entries({
            '/dir/file': 'value',
            '/dir/.other': 'incorrect',
            '/dir/other': 'content'
        })

        self.assertEqual({
            'file': 'value',
            'other': 'content'
        }, parse(['/dir']))

    def test_parse_skips_directories_nested_in_directory(self):
        self.mockfs.add_entries({
            '/dir/file': 'value',
            '/dir/nested/file': 'incorrect',
            '/dir/other': 'content'
        })

        self.assertEqual({
            'file': 'value',
            'other': 'content'
        }, parse(['/dir']))

    def test_parse_parses_all_paths_given(self):
        self.mockfs.add_entries({
            '/some/file': 'value',
            '/other/complex': '''\
key1="value1"
key2="value2"
'''
        })

        self.assertEqual({
            'file': 'value',
            'complex': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }, parse(['/some/file', '/other/complex']))
