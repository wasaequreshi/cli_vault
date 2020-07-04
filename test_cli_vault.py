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
        args = SimpleNamespace(command="command",description="description",tags="tags")
        self.sv.add(args)
        
        command_data = {}
        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            
            self.assertTrue(len(data) == 1)
            self.assertTrue(data[0]['command'] == "command" and data[0]['description'] == "description" and data[0]['tags'] == ["tags"])

        args = SimpleNamespace(command="command1",description=None,tags="tags1")
        self.sv.add(args)

        command_data = {}
        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            
            self.assertTrue(len(data) == 2)
            self.assertTrue(data[1]['command'] == "command1" and data[1]['description'] == "" and data[1]['tags'] == ["tags1"])

        args = SimpleNamespace(command="command2",description=None,tags="tags1,tags2")
        self.sv.add(args)

        command_data = {}
        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            
            self.assertTrue(len(data) == 3)
            self.assertTrue(data[2]['command'] == "command2" and data[2]['description'] == "" and data[2]['tags'] == ["tags1", "tags2"])
    
    def test_delete(self):
        
        args = SimpleNamespace(command="command",description="description",tags="tags")
        self.sv.add(args)
        args = SimpleNamespace(command="command1",description=None,tags="tags1")
        self.sv.add(args)
        args = SimpleNamespace(command="command2",description=None,tags="tags1,tags2")
        self.sv.add(args)

        ids = []

        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            self.assertTrue(len(data) == 3)

            for d in data:
                ids.append(d['id'])

        args = SimpleNamespace(command_id=ids[0])
        self.sv.delete(args)

        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            self.assertTrue(len(data) == 2)

    def test_update(self):

        args = SimpleNamespace(command="command",description="description",tags="tags")
        self.sv.add(args)
        args = SimpleNamespace(command="command1",description=None,tags="tags1")
        self.sv.add(args)
        args = SimpleNamespace(command="command2",description=None,tags="tags1,tags2")
        self.sv.add(args)

        ids = []
        
        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            self.assertTrue(len(data) == 3)

            for d in data:
                ids.append(d['id'])

        args = SimpleNamespace(command_id=ids[0], command="command19",description=None,tags=None)
        self.sv.update(args)
        
        with open(os.path.join('.secure_vault', 'commands.json')) as json_file:
            command_data = json.load(json_file)
            data = command_data['data']
            self.assertTrue(len(data) == 3)
            self.assertTrue(data[0]['command'] == "command19" and data[0]['description'] == "description" and data[0]['tags'] == ["tags"])

    def tearDown(self):
        dir_path = os.path.join(".secure_vault")
        shutil.rmtree(dir_path)

if __name__ == '__main__':
    unittest.main()