#!/usr/bin/env python3
#pylint: disable=duplicate-code
"""Tests for anmad.yaml module."""

import logging
import os
import unittest

import __main__ as main

import anmad.common.yaml

class TestYaml(unittest.TestCase):
    """Tests for anmad_buttons module."""

    def setUp(self):
        self.playbooks = ['deploy.yaml', 'deploy2.yaml']
        self.pre_run_playbooks = ['deploy4.yaml']
        self.playbookroot = '/vagrant/samples'
        self.logger = logging.getLogger(os.path.basename(main.__file__))
        # Change logging.ERROR to INFO, to see log messages during testing.
        self.logger.setLevel(logging.CRITICAL)
        self.testyamlfiles = ['deploy.yaml']
        for num in range(2, 9):
            dnum = [('deploy' + str(num) + '.yaml')]
            self.testyamlfiles.extend(dnum)
        self.testyamlfiles.extend(['deploy9.yml'])
        self.testyamlfiles_parent = ['/vagrant/samples/' + x for x in self.testyamlfiles]
        self.testyamlfiles_parent.sort()

    def test_find_yaml_files(self):
        """Test find_yaml_files func."""
        yamlfiles = anmad.common.yaml.find_yaml_files(self.logger, self.playbookroot)
        self.assertIsNotNone(yamlfiles)
        self.assertEqual(len(yamlfiles), 9)
        self.assertEqual(yamlfiles, self.testyamlfiles_parent)

    def test_verify_yaml_missingfile(self):
        """Test verify_yaml with missing file."""
        verify = anmad.common.yaml.verify_yaml_file(self.logger, '/vagrant/test/missing.yml')
        self.assertFalse(verify)

    def test_verify_yaml_is_empty_directory(self):
        """Test verify_yaml with empty dir."""
        verify = anmad.common.yaml.verify_yaml_file(self.logger, '/vagrant/empty_dir')
        self.assertFalse(verify)

    def test_verify_yaml_is_directory(self):
        """Test verify_yaml with a dir containing stuff."""
        verify = anmad.common.yaml.verify_yaml_file(self.logger, '/vagrant/samples')
        self.assertTrue(verify)

    def test_verify_yaml_is_bad_directory(self):
        """Test verify_yaml_file with a dir containing bad yaml."""
        verify = anmad.common.yaml.verify_yaml_file(self.logger, 'test')
        self.assertFalse(verify)

    def test_verify_yaml_goodfile(self):
        """Test verify_yaml_file func with valid yaml."""
        verify = anmad.common.yaml.verify_yaml_file(
            self.logger,
            (self.playbookroot + '/' + self.playbooks[0]))
        self.assertTrue(verify)

    def test_verify_yaml_badfile(self):
        """Test that verify_yaml_file correctly identifies bad yaml."""
        verify = anmad.common.yaml.verify_yaml_file(self.logger, '/vagrant/test/badyaml.yml')
        self.assertFalse(verify)

    def test_list_bad_yamlfiles(self):
        """Test that bad yamlfiles are listed."""
        verify = anmad.common.yaml.list_bad_yamlfiles(self.logger, ['test'])
        self.assertEqual(verify, ['test'])

    def test_list_bad_yamlfiles_allgood(self):
        """Test that list_bad_yamlfiles returns empty string when it should."""
        verify = anmad.common.yaml.list_bad_yamlfiles(self.logger, ['/vagrant/samples'])
        self.assertEqual(verify, [])

    def test_list_missing_files(self):
        """Test missing files func."""
        testfiles = ['/vagrant/samples/' + x for x in self.playbooks]
        verify = anmad.common.yaml.list_bad_yamlfiles(self.logger, testfiles)
        self.assertEqual(verify, [])
        verify = anmad.common.yaml.list_bad_yamlfiles(self.logger, ['/vagrant/test/missing.yml'])
        self.assertEqual(verify, ['/vagrant/test/missing.yml'])

    def test_verify_config_file(self):
        """Test the verify_config_file func."""
        verify = anmad.common.yaml.verify_config_file('/vagrant/test/bad-inventory')
        self.assertFalse(verify)
        verify = anmad.common.yaml.verify_config_file('/vagrant/samples/inventory-internal')
        self.assertTrue(verify)


if __name__ == '__main__':
    unittest.main()
