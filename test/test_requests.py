#!/usr/bin/env python3
"""Test http return codes."""

import unittest
import re
import datetime

import requests

class TestReturnCodes(unittest.TestCase):
    """Test http return codes."""

    def setUp(self):
        self.baseurl = "http://localhost:9999/"
        self.dateformat = "%Y-%m-%d %H:%M:%S"

    def test_clearall_button(self):
        """Test the clearall button."""
        output = requests.get(self.baseurl + 'clearqueues')
        self.assertEqual(200, output.status_code)
        self.assertIn('Clear redis queues requested.', output.text)

    def test_runall_button(self):
        """Test the runall button."""
        # pylint: disable=C0301
        requests.get(self.baseurl + 'clearqueues')
        output = requests.get(self.baseurl + 'runall')
        self.assertEqual(200, output.status_code)
        self.assertIn("Jobs in queue", output.text)
        self.assertIn("/vagrant/samples/deploy.yaml&#39;, &#39;/vagrant/samples/deploy2.yaml&#39;]</h3>", output.text)
        self.assertIn(
            "[&#39;/vagrant/samples/deploy4.yaml&#39;]</h3>", output.text)

    def test_otherplays(self):
        """Test the otherplays page."""
        output = requests.get(self.baseurl + 'otherplays')
        self.assertEqual(200, output.status_code)
        self.assertIn("run deploy6.yaml", output.text)
        self.assertIn("run deploy9.yml", output.text)
        self.assertIn("Other playbooks in root dir", output.text)

    def test_jobs(self):
        """Test the jobs / processes page."""
        output = requests.get(self.baseurl + 'jobs')
        self.assertEqual(200, output.status_code)
        self.assertIn("/srv/config/deploy.yaml", output.text)
        self.assertIn("/srv/config/deploy2.yaml", output.text)
        self.assertIn("self.location.href='/ansiblelog?play=deploy.yaml&latest=True'", output.text)
        self.assertIn("self.location.href='/ansiblelog?play=deploy2.yaml&latest=True'", output.text)
        self.assertIn("Home", output.text)
        self.assertIn("KILL PID", output.text)
        self.assertIn("Kill all running jobs", output.text)

    def test_log(self):
        """Test the log page."""
        output = requests.get(self.baseurl + 'log')
        self.assertEqual(200, output.status_code)
        self.assertIn("for full logs, check syslog", output.text)
        self.assertIn("messages (newest first):", output.text)

    def test_log_list(self):
        """Test the log list page."""
        output = requests.get(self.baseurl + 'ansiblelog?play=')
        self.assertEqual(200, output.status_code)
        self.assertIn("deploy.yaml", output.text)
        self.assertIn("deploy9.yml", output.text)
        output = requests.get(self.baseurl + 'ansiblelog?play=..')
        self.assertEqual(403, output.status_code)
        output = requests.get(self.baseurl + 'ansiblelog?play=/..')
        self.assertEqual(403, output.status_code)
        output = requests.get(self.baseurl + 'ansiblelog?play=/../')
        self.assertEqual(403, output.status_code)

    def test_ansiblelog(self):
        """Test that latest log uris work."""
        output = requests.get(self.baseurl + 'ansiblelog?play=deploy4.yaml&latest=True')
        self.assertEqual(200, output.status_code)
        self.assertIn("deploy4.yaml", output.text)
        output = requests.get(self.baseurl + 'ansiblelog?play=deploy.yaml&latest=True')
        self.assertEqual(200, output.status_code)
        self.assertIn("deploy.yaml", output.text)

    def test_gitpull(self):
        """Test that /gitpull errors and that it redirects to /"""
        output = requests.get(self.baseurl + 'gitpull')
        self.assertEqual(200, output.status_code)
        self.assertIn("Other Playbooks", output.text)
        output = requests.get(self.baseurl + 'log')
        self.assertIn("git pull: Already up to date.", output.text)

if __name__ == '__main__':
    unittest.main()
