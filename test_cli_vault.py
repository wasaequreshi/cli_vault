import unittest
from cli_vault import cli_vault
class TestCliVault(unittest.TestCase):

    def setUp(self):
        self.sv = cli_vault(True)
    
    def test_add(self):
        pass

if __name__ == '__main__':
    unittest.main()