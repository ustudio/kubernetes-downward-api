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
