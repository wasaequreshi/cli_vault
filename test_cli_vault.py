import unittest
from cli_vault import cli_vault
from pathlib import Path
import shutil
import os
from types import SimpleNamespace
import json

class TestCliVault(unittest.TestCase):

    def setUp(self):
        self.sv = cli_vault(True)
    
    def test_add(self):
        args = SimpleNamespace(cli_note="cli_note",description="description",tags="tags")
        self.sv.add(args)
        
        cli_note_data = {}
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            
            self.assertTrue(len(data) == 1)
            self.assertTrue(data[0]['cli_note'] == "cli_note" and data[0]['description'] == "description" and data[0]['tags'] == ["tags"])

        args = SimpleNamespace(cli_note="cli_note1",description=None,tags="tags1")
        self.sv.add(args)

        cli_note_data = {}
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            
            self.assertTrue(len(data) == 2)
            self.assertTrue(data[1]['cli_note'] == "cli_note1" and data[1]['description'] == "" and data[1]['tags'] == ["tags1"])

        args = SimpleNamespace(cli_note="cli_note2",description=None,tags="tags1,tags2")
        self.sv.add(args)

        cli_note_data = {}
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            
            self.assertTrue(len(data) == 3)
            self.assertTrue(data[2]['cli_note'] == "cli_note2" and data[2]['description'] == "" and data[2]['tags'] == ["tags1", "tags2"])
    
    def test_delete(self):
        
        args = SimpleNamespace(cli_note="cli_note",description="description",tags="tags")
        self.sv.add(args)
        args = SimpleNamespace(cli_note="cli_note1",description=None,tags="tags1")
        self.sv.add(args)
        args = SimpleNamespace(cli_note="cli_note2",description=None,tags="tags1,tags2")
        self.sv.add(args)

        ids = []

        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 3)

            for d in data:
                ids.append(d['id'])

        args = SimpleNamespace(cli_note_id=ids[0])
        self.sv.delete(args)

        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 2)

    def test_update(self):

        args = SimpleNamespace(cli_note="cli_note",description="description",tags="tags")
        self.sv.add(args)
        args = SimpleNamespace(cli_note="cli_note1",description=None,tags="tags1")
        self.sv.add(args)
        args = SimpleNamespace(cli_note="cli_note2",description=None,tags="tags1,tags2")
        self.sv.add(args)

        ids = []
        
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 3)

            for d in data:
                ids.append(d['id'])

        args = SimpleNamespace(cli_note_id=ids[0], cli_note="cli_note19",description=None,tags=None)
        self.sv.update(args)
        
        with open(os.path.join('.secure_vault', 'cli_notes.json')) as json_file:
            cli_note_data = json.load(json_file)
            data = cli_note_data['data']
            self.assertTrue(len(data) == 3)
            self.assertTrue(data[0]['cli_note'] == "cli_note19" and data[0]['description'] == "description" and data[0]['tags'] == ["tags"])

    def tearDown(self):
        dir_path = os.path.join(".secure_vault")
        shutil.rmtree(dir_path)

if __name__ == '__main__':
    unittest.main()