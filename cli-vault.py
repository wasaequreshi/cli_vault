#!/usr/bin/env python3

import os
import json
import sys
import pprint
import uuid
import argparse
from pathlib import Path
import string
from nltk.corpus import stopwords
import nltk
import string

class cli_vault:

    # configuration setup
    sv_dir = ".secure_vault"
    sv_command_file = "commands.json"

    # If folders and files aren't setup, then on each run make sure to do so
    def __init__(self):

        # Setting up directory in home and file inside that directory
        self.sv_dir_path = os.path.join(str(Path.home()), self.sv_dir)
        self.sv_command_file_path = os.path.join(str(Path.home()), self.sv_dir, self.sv_command_file)
        
        # Checking if directory exists or not, create it otherwise
        if not os.path.isdir(self.sv_dir_path):
            os.makedirs(self.sv_dir_path)
        
        # Check if file exists of not, create it otherwise
        if not os.path.isfile(self.sv_command_file_path):
            command_data = {'data' : []}
            with open(self.sv_command_file_path, 'w') as outfile:
                json.dump(command_data, outfile, indent=4)
    
    def remove_stopwords(self, text):
        nltk.download('stopwords', quiet=True)
        stopword = set(stopwords.words('english'))

        text = [word for word in text if word not in stopword]
        return ' '.join(text)

    def remove_punctuation(self, text):
        no_punct = [words for words in text if words not in string.punctuation]
        words_wo_punct = ''.join(no_punct)
        return words_wo_punct

    # Command to add a command/note
    def add(self, args):
        # Getting arguments
        command = args.command
        description = args.description if args.description else ""
        tags = args.tags if args.tags else ""
        
        # Need to check this each time, file could be corrupt which can cause program to crash
        if self.is_valid_file_path():
            # Loading data
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                # Creating new data
                new_data = {"id" : str(uuid.uuid4())[:8], "command" : command, "description" : description, "tags" : tags.split(",")}
                
                # Appending to loaded data
                command_data['data'].append(new_data)

                # Writing back to file
                with open(self.sv_command_file_path, 'w') as outfile:
                    json.dump(command_data, outfile, indent=4)

    # Deletes a stored command/note
    def delete(self, args):
        # Getting arguments
        command_id = args.command_id
        # Loading data
        if self.is_valid_file_path():
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                # Setting up data
                new_data = []
                id_found = False

                # Checking which data to not add
                for data in command_data['data']:
                    if not data['id'] == command_id:
                        new_data.append(data)
                    else:
                        id_found = True
                # Update data store
                command_data['data'] = new_data
                
                #Write back to file
                with open(self.sv_command_file_path, 'w') as outfile:
                    json.dump(command_data, outfile, indent=4)

                # Print if it was found or not
                if id_found:
                    print("Command deleted")
                else:
                    print("Invalid id")

    # Similar to ls, shows all the commands stored
    def list_commands(self, args):
        # Just loading the file
        if self.is_valid_file_path():
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                # Doing a json pretty print
                print(json.dumps(command_data['data'], indent=4, sort_keys=True))

    # Validator to make sure files/config is okay to load
    def is_valid_file_path(self):
        if os.path.isfile(self.sv_command_file_path):
            return True
        else:
            print ("Script vault dir corrupted, remove " + self.sv_dir_path)


    # Searching for command/notes
    def search(self, args):
        # Getting arguments 
        contents = args.content if args.content else ""
        # contents = contents.split(" ")
        # contents = self.remove_stopwords(contents)
        # contents = self.remove_punctuation(contents)
        
        tags = args.tags if args.tags else ""
        tags = tags.split(",")
        # Loading file
        if self.is_valid_file_path():
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                results_seen = []
                results = []
                # Searching via content ind command and description
                if contents != "":
                    contents = contents.split(" ")
                    for content in contents:
                        for data in command_data['data']: 
                            if (content in data['command'] or content in data['description'] or content in data['tags']) and data['id'] not in results_seen:
                                results.append(data)
                                results_seen.append(data['id'])

                # Searching via tags
                if tags != "":
                    for tag in tags:
                        for data in command_data['data']:
                            if tag in data['tags'] and data['id'] not in results_seen:
                                results.append(data)
                                results_seen.append(data['id'])

                print(json.dumps(results, indent=4, sort_keys=True))

    def update(self, args):
        # Getting arguments
        command = args.command
        description = args.description
        tags = args.tags
        command_id = args.command_id
        # Loading data
        if self.is_valid_file_path():
            command_data = {}
            with open(self.sv_command_file_path) as json_file:
                command_data = json.load(json_file)
                
                # Setting up data
                new_data = []
                id_found = False

                # Checking which data to not add
                for data in command_data['data']:
                    if data['id'] == command_id:
                        id_found = True
                        if command != None:
                            data['command'] = command
                        if description != None:
                            data['description'] = description
                        if tags != None:
                            data['tags'] = tags.split(",")
                
                #Write back to file
                with open(self.sv_command_file_path, 'w') as outfile:
                    json.dump(command_data, outfile, indent=4)

                # Print if it was found or not
                if id_found:
                    print("Updated")
                else:
                    print("Invalid id")

# Add argument parser to handle params and options
if __name__ == "__main__":
    
    # Creating instance of class
    sv = cli_vault()

    # Argument parser to handle arguments for different subcommands and flags
    parser = argparse.ArgumentParser(prog='cli-vault', description="Store cli commands or other notes with our tool.")
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "add, delete, list, or search"
    
    # Add command setup
    parser_add = subparsers.add_parser('add', help='Allows you to add a cli command/note')
    parser_add.add_argument('-c', '--command', metavar="<command>", help='command/note to store', required=True)
    parser_add.add_argument('-d', '--description', metavar="<description>", help='description of the command/note. Used for search')
    parser_add.add_argument('-t', '--tags', metavar="<tags>", help='tags of command to categorize commands. Used for search')
    parser_add.set_defaults(func=sv.add)

    # Delete command setup
    parser_delete = subparsers.add_parser('delete', help='Allows you to remote a cli command/note')
    parser_delete.add_argument('-id', '--command_id', help='command/note to delete', required=True)
    parser_delete.set_defaults(func=sv.delete)
    
    # List command setup
    parser_list = subparsers.add_parser('list', help='Shows stored commands/notes')
    parser_list.set_defaults(func=sv.list_commands)

    # Search command setup
    parser_search = subparsers.add_parser('search', help='Search for stored commands/notes')
    parser_search.add_argument('-c', '--content', help='Text to search for')
    parser_search.add_argument('-t', '--tags', help='Tags to search for')
    parser_search.set_defaults(func=sv.search)

    # Update command setup
    parser_update = subparsers.add_parser('update', help='Allows you to update a cli command/note')
    parser_update.add_argument('-id', '--command_id', help='command/note to delete', required=True)
    parser_update.add_argument('-c', '--command', metavar="<command>", help='command/note to update')
    parser_update.add_argument('-d', '--description', metavar="<description>", help='description of the command/note. Used for search')
    parser_update.add_argument('-t', '--tags', metavar="<tags>", help='tags of command to categorize commands. Used for search')
    parser_update.set_defaults(func=sv.update)

    # Running arg parser
    args = parser.parse_args()
    args.func(args)