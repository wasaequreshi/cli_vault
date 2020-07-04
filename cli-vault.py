#!/usr/bin/env python3

import os
import json
import sys
import pprint
import uuid
import argparse
from pathlib import Path

class cli_vault:

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
    
    def add(self, args):
        command = args.command
        description = args.description if args.description else ""
        tags = args.tags if args.tags else ""
        
        if self.is_valid_file_path():
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                new_data = {"id" : str(uuid.uuid4())[:8] ,"command" : command, "description" : description, "tags" : tags.split(",")}
                
                command_data['data'].append(new_data)

                with open(self.sv_command_file_path, 'w') as outfile:
                    json.dump(command_data, outfile, indent=4)

    def list_commands(self, args):
        if self.is_valid_file_path():
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                print(json.dumps(command_data['data'], indent=4, sort_keys=True))
    
    def delete(self, args):
        command_id = args.command_id
        if self.is_valid_file_path():
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

    def is_valid_file_path(self):
        if os.path.isfile(self.sv_command_file_path):
            return True
        else:
            print ("Script vault dir corrupted, remove " + self.sv_dir_path)


    # Implement search on existing data
    def search(self, args):
        content = args.content if args.content else ""
        tags = args.tags if args.tags else ""

        if self.is_valid_file_path():
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)

    # Implement automatically storing command data

# Add argument parser to handle params and options
if __name__ == "__main__":
    sv = cli_vault()

    parser = argparse.ArgumentParser(prog='cli-vault', description="Store cli commands or other notes with our tool.")
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "add, delete, list, or search"
    
    parser_add = subparsers.add_parser('add', help='Allows you to add a cli command/note')
    parser_add.add_argument('-c', '--command', metavar="<command>", help='command/note to store', required=True)
    parser_add.add_argument('-d', '--description', metavar="<description>", help='description of the command/note. Used for search')
    parser_add.add_argument('-t', '--tags', metavar="<tags>", help='tags of command to categorize commands. Used for search')
    parser_add.set_defaults(func=sv.add)

    parser_delete = subparsers.add_parser('delete', help='Allows you to remote a cli command/note')
    parser_delete.add_argument('-id', '--command_id', help='command/note to delete', required=True)
    parser_delete.set_defaults(func=sv.delete)
    
    parser_list = subparsers.add_parser('list', help='Shows stored commands/notes')
    parser_list.set_defaults(func=sv.list_commands)

    parser_search = subparsers.add_parser('search', help='Search for stored commands/notes')
    parser_search.add_argument('-c', '--content', help='Text to search for')
    parser_search.add_argument('-t', '--tags', help='Tags to search for')
    parser_search.set_defaults(func=sv.search)

    args = parser.parse_args()
    args.func(args)