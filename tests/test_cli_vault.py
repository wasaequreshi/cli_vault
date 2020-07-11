import unittest
import shutil
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from pathlib import Path
from cli_vault import cli_vault
from types import SimpleNamespace

class TestCliVault(unittest.TestCase):

    def setUp(self):
        self.sv = cli_vault(True)
    
    def test_add(self):
        args = SimpleNamespace(cli_note="cli_note",description="description",tags="tags")
        self.sv._add(args)
        
        cli_note_data = {}
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            
            self.assertTrue(len(data) == 1)
            self.assertTrue(data[0]['cli_note'] == ["cli_note"] and data[0]['description'] == ["description"] and data[0]['tags'] == ["tags"])

        args = SimpleNamespace(cli_note="cli_note1",description=None,tags="tags1")
        self.sv._add(args)

        cli_note_data = {}
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 2)
            self.assertTrue(data[1]['cli_note'] == ["cli_note1"] and data[1]['description'] == [""] and data[1]['tags'] == ["tags1"])

        args = SimpleNamespace(cli_note="cli_note2",description=None,tags="tags1,tags2")
        self.sv._add(args)

        cli_note_data = {}
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            
            self.assertTrue(len(data) == 3)
            self.assertTrue(data[2]['cli_note'] == ["cli_note2"] and data[2]['description'] == [""] and data[2]['tags'] == ["tags1", "tags2"])
    
    def test_delete(self):
        
        args = SimpleNamespace(cli_note="cli_note",description="description",tags="tags")
        self.sv._add(args)
        args = SimpleNamespace(cli_note="cli_note1",description=None,tags="tags1")
        self.sv._add(args)
        args = SimpleNamespace(cli_note="cli_note2",description=None,tags="tags1,tags2")
        self.sv._add(args)

        ids = []

        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 3)

            for d in data:
                ids.append(d['id'])

        args = SimpleNamespace(cli_note_id=ids[0])
        self.sv._delete(args)

        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 2)

    def test__update(self):

        args = SimpleNamespace(cli_note="cli_note",description="description",tags="tags")
        self.sv._add(args)
        args = SimpleNamespace(cli_note="cli_note1",description=None,tags="tags1")
        self.sv._add(args)
        args = SimpleNamespace(cli_note="cli_note2",description=None,tags="tags1,tags2")
        self.sv._add(args)

        ids = []
        
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 3)

            for d in data:
                ids.append(d['id'])
 
        args = SimpleNamespace(cli_note_id=ids[0], cli_note="cli_note19",description=None,tags=None)
        self.sv._update(args)
        
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 3)
            self.assertTrue(data[0]['cli_note'] == ["cli_note19"] and data[0]['description'] == ["description"] and data[0]['tags'] == ["tags"])

    def test_search(self):
        args = SimpleNamespace(cli_note="ssh -i my_private_key ubuntu@localhost",description="ssh into server with private key",tags="ssh,private key,unique")
        self.sv._add(args)

        args = SimpleNamespace(text='into', a=False, c=False, d=False, t=False)

        results = self.sv._search(args)

        self.assertTrue(results[0]['cli_note'] == ["ssh -i my_private_key ubuntu@localhost"] and results[0]['description'] == ["ssh into server with private key"] and results[0]['tags'] == ["ssh","private key","unique"])

        args = SimpleNamespace(text='unique', a=True, c=False, d=False, t=False)

        results = self.sv._search(args)

        self.assertTrue(results[0]['cli_note'] == ["ssh -i my_private_key ubuntu@localhost"] and results[0]['description'] == ["ssh into server with private key"] and results[0]['tags'] == ["ssh","private key","unique"])

        args = SimpleNamespace(text='my_private_key', a=False, c=True, d=False, t=False)

        results = self.sv._search(args)

        self.assertTrue(results[0]['cli_note'] == ["ssh -i my_private_key ubuntu@localhost"] and results[0]['description'] == ["ssh into server with private key"] and results[0]['tags'] == ["ssh","private key","unique"])

        args = SimpleNamespace(text='unique', a=False, c=True, d=False, t=False)

        results = self.sv._search(args)

        self.assertTrue(len(results) == 0)

        args = SimpleNamespace(text='into', a=False, c=False, d=True, t=False)

        results = self.sv._search(args)

        self.assertTrue(results[0]['cli_note'] == ["ssh -i my_private_key ubuntu@localhost"] and results[0]['description'] == ["ssh into server with private key"] and results[0]['tags'] == ["ssh","private key","unique"])
        
        args = SimpleNamespace(text='unique', a=False, c=False, d=True, t=False)

        results = self.sv._search(args)

        self.assertTrue(len(results) == 0)

        args = SimpleNamespace(text='unique', a=False, c=False, d=False, t=True)

        results = self.sv._search(args)

        self.assertTrue(results[0]['cli_note'] == ["ssh -i my_private_key ubuntu@localhost"] and results[0]['description'] == ["ssh into server with private key"] and results[0]['tags'] == ["ssh","private key","unique"])
        
        args = SimpleNamespace(text='into', a=False, c=False, d=False, t=True)

        results = self.sv._search(args)

        self.assertTrue(len(results) == 0)

    def test_list(self):
        
        results = self.sv._list_cli_notes(None)

        self.assertTrue(len(results['data']) == 0)

        args = SimpleNamespace(cli_note="ssh -i my_private_key ubuntu@localhost",description="ssh into server with private key",tags="ssh,private key,unique")
        self.sv._add(args)
        args = SimpleNamespace(cli_note="ssh -i my_private_key ubuntu@localhost",description="ssh into server with private key",tags="ssh,private key,unique")

        results = self.sv._list_cli_notes(None)
        # print(results)
        self.assertTrue(results['data'][0]['cli_note'] == ["ssh -i my_private_key ubuntu@localhost"] and results['data'][0]['description'] == ["ssh into server with private key"] and results['data'][0]['tags'] == ["ssh","private key","unique"])

    def tearDown(self):
        dir_path = os.path.join(".secure_vault")
        shutil.rmtree(dir_path)

if __name__ == '__main__':
    unittest.main()