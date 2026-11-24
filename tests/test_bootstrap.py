import importlib.util
import subprocess
import sys
import unittest

class BootstrapTests(unittest.TestCase):
    def test_installed_cli_starts_without_credentials(self):
        self.assertIsNotNone(importlib.util.find_spec('starbots_hybrid'), 'Hybrid package is not implemented')
        process = subprocess.run([sys.executable, '-m', 'starbots_hybrid.cli', '--help'], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn('sb-hybrid', process.stdout)

if __name__ == '__main__':
    unittest.main()
