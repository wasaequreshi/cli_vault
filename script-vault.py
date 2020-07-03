import os
from pathlib import Path
import json
import sys
import pprint
import uuid

class script_vault:

    sv_dir = ".secure_vault"
    sv_command_file = "commands.json"

    def __init__(self):

        self.sv_dir_path = os.path.join(str(Path.home()), self.sv_dir)
        self.sv_command_file_path = os.path.join(str(Path.home()), self.sv_dir, self.sv_command_file)
        
        if not os.path.isdir(self.sv_dir_path):
            os.makedirs(self.sv_dir_path)
        
        if not os.path.isfile(self.sv_command_file_path):
            command_data = {'data' : []}
            with open(self.sv_command_file_path, 'w') as outfile:
                json.dump(command_data, outfile, indent=4)
    
    def add(self, command, description="", tags=""):
        if os.path.isfile(self.sv_command_file_path):
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                new_data = {"id" : str(uuid.uuid4())[:8] ,"command" : command, "description" : description, "tags" : tags}
                
                command_data['data'].append(new_data)

                with open(self.sv_command_file_path, 'w') as outfile:
                    json.dump(command_data, outfile, indent=4)
        else:
            print ("Script vault dir corrupted, remove " + self.sv_dir_path)

    def list(self):
         if os.path.isfile(self.sv_command_file_path):
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                print(json.dumps(command_data['data'], indent=4, sort_keys=True))

    def delete(self, command_id):
        if os.path.isfile(self.sv_command_file_path):
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                new_data = []

                id_found = False

                for data in command_data['data']:
                    if not data['id'] == command_id:
                        new_data.append(data)
                    else:
                        id_found = True
                      
                command_data['data'] = new_data
                
                with open(self.sv_command_file_path, 'w') as outfile:
                    json.dump(command_data, outfile, indent=4)

                if id_found:
                    print("Command deleted")
                else:
                    print("Invalid id")

    def search(self):
        pass
    
if __name__ == "__main__":
    sv = script_vault()
    if len(sys.argv) == 1:
        print ("Show help")
    else:
        command = sys.argv[1]

        if command == "add":
            sv.add("test", "test", "test")
        elif command == "list":
            sv.list()
        elif command == "delete":
            sv.delete("c809d0f8")