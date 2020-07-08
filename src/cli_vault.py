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
from pygments import highlight, lexers, formatters
import tempfile
from subprocess import call

class cli_vault:

    # configuration setup
    sv_dir = ".secure_vault"
    sv_cli_note_file = "cli_notes.json"

    # If folders and files aren't setup, then on each run make sure to do so
    def __init__(self, is_test=False):

        if not is_test:
            # Setting up directory in home and file inside that directory
            self.sv_dir_path = os.path.join(str(Path.home()), self.sv_dir)
            self.sv_cli_note_file_path = os.path.join(str(Path.home()), self.sv_dir, self.sv_cli_note_file)
            
            # Checking if directory exists or not, create it otherwise
            if not os.path.isdir(self.sv_dir_path):
                os.makedirs(self.sv_dir_path)
            
            # Check if file exists of not, create it otherwise
            if not os.path.isfile(self.sv_cli_note_file_path):
                cli_note_data = {'data' : []}
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)
        else:
            self.sv_dir_path = self.sv_dir
            self.sv_cli_note_file_path = os.path.join(self.sv_dir, self.sv_cli_note_file)
            # Checking if directory exists or not, create it otherwise
            if not os.path.isdir(self.sv_dir_path):
                os.makedirs(self.sv_dir_path)
            
            # Check if file exists of not, create it otherwise
            if not os.path.isfile(self.sv_cli_note_file_path):
                cli_note_data = {'data' : []}
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)

    # Search idea for later
    def remove_stopwords(self, text):
        nltk.download('stopwords', quiet=True)
        stopword = set(stopwords.words('english'))

        text = [word for word in text if word not in stopword]
        return ' '.join(text)

    # Search idea for later
    def remove_punctuation(self, text):
        no_punct = [words for words in text if words not in string.punctuation]
        words_wo_punct = ''.join(no_punct)
        return words_wo_punct

    # Validator to make sure files/config is okay to load
    def is_valid_file_path(self):
        if os.path.isfile(self.sv_cli_note_file_path):
            return True
        else:
            print ("Script vault dir corrupted, remove " + self.sv_dir_path)

    def pretty_print(self, cli_note_data):
        formatted_json = json.dumps(cli_note_data['data'], indent=4, sort_keys=True)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)

    def vim_editor(self, current):
        initial_message = current
        tf = tempfile.NamedTemporaryFile('w+', suffix=".tmp", delete=False)
        tf.write(initial_message)
        tf.close()

        call(['vim', tf.name])

        tf = open(tf.name, 'r')
        edited_message = tf.readlines()
        edited_message = [e_message.strip("\n") for e_message in edited_message]
        edited_message = ' '.join(edited_message)
        
        tf.close()

        os.unlink(tf.name)

        return edited_message

    def vim(self, cli_note, description, tags):

        cli_note = self.vim_editor("<cli note>" if cli_note == "" else cli_note)
        description = self.vim_editor("<description>" if description == "" else description)
        tags = self.vim_editor("<tags comma separated>" if tags == "" else tags)

        return cli_note, description, tags
    
    def vim_add(self, cli_note, description, tags):
        return self.vim(cli_note, description, tags)

    def vim_update(self, cli_note, description, tags):
        return self.vim(cli_note, description, ','.join(tags))

    # cli_note to add
    def add(self, args):
        # Getting arguments
        cli_note = args.cli_note if args.cli_note else ""
        description = args.description if args.description else ""
        tags = args.tags if args.tags else ""
        
        # If all blank, open vim for each
        if cli_note == "":
            cli_note, description, tags = self.vim_add(cli_note, description, tags)
        
        # Need to check this each time, file could be corrupt which can cause program to crash
        if self.is_valid_file_path():
            # Loading data
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                # Creating new data
                new_data = {"id" : str(uuid.uuid4())[:8], "cli_note" : cli_note, "description" : description, "tags" : tags.split(",")}
                
                # Appending to loaded data
                cli_note_data['data'].append(new_data)

                # Writing back to file
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)

    # Deletes a stored cli_note
    def delete(self, args):
        # Getting arguments
        cli_note_id = args.cli_note_id
        # Loading data
        if self.is_valid_file_path():
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                # Setting up data
                new_data = []
                id_found = False

                # Checking which data to not add
                for data in cli_note_data['data']:
                    if not data['id'] == cli_note_id:
                        new_data.append(data)
                    else:
                        id_found = True
                
                # Update data store
                cli_note_data['data'] = new_data
                
                #Write back to file
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)

                # Print if it was found or not
                if id_found:
                    print("Cli note deleted")
                else:
                    print("Invalid id")
    
    # Updating stored cli_note
    def update(self, args):
        # Getting arguments
        cli_note = args.cli_note
        description = args.description
        tags = args.tags
        cli_note_id = args.cli_note_id

        if cli_note == None and description == None and tags == None:
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                # Checking which data to update
                for data in cli_note_data['data']:
                    if data['id'] == cli_note_id:
                        cli_note, description, tags = self.vim_update(data['cli_note'], data['description'], data['tags'])

        # Loading data
        if self.is_valid_file_path():
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                # Setting up data
                id_found = False

                # Checking which data to update
                for data in cli_note_data['data']:
                    if data['id'] == cli_note_id:
                        if cli_note != None:
                            data['cli_note'] = cli_note
                        if description != None:
                            data['description'] = description
                        if tags != None:
                            data['tags'] = tags.split(",")
                        id_found = True
                #Write back to file
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)

                # Print if it was updated or not
                if id_found:
                    print("Updated")
                else:
                    print("Invalid id")

    # Similar to ls, shows all the cli_notes stored
    def list_cli_notes(self, args):
        # Just loading the file
        if self.is_valid_file_path():
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                # Doing a json pretty print
                self.pretty_print(cli_note_data)

    # Searching for cli_notes
    def search(self, args):
        # Getting arguments 
        text_all = args.all if args.all else ""
        text_cli_note = args.cli_note if args.cli_note else ""
        text_description = args.description if args.description else ""
        text_tags = args.tags if args.tags else ""

        # No need to search for other flags
        if text_all:
            text_cli_note = ""
            text_description = ""
            text_tags = ""
        # Need to ask for advice on whether to keep this, this does improve 
        # performance, but ruins accuracy :(
        # contents = contents.split(" ")
        # contents = self.remove_stopwords(contents)
        # contents = self.remove_punctuation(contents)
        
        # Loading file
        if self.is_valid_file_path():
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                results_seen = []
                results = []
                # Searching all
                if text_all != "":
                    text_all = text_all.split(" ")
                    for word in text_all:
                        for data in cli_note_data['data']: 
                            if (word.lower() in data['cli_note'].lower() or word.lower() in data['description'].lower() or word.lower() in [each_tag.lower() for each_tag in data['tags']]) and data['id'] not in results_seen:
                                results.append(data)
                                results_seen.append(data['id'])

                # Searching via cli_note
                if text_cli_note != "":
                    text_cli_note = text_cli_note.split(" ")
                    for cli_note in text_cli_note:
                        for data in cli_note_data['data']:
                            if cli_note.lower() in data['cli_note'].lower() and data['id'] not in results_seen:
                                results.append(data)
                                results_seen.append(data['id'])
                
                # Searching via description
                if text_description != "":
                    text_description = text_description.split(" ")
                    for description in text_description:
                        for data in cli_note_data['data']:
                            if description.lower() in data['description'].lower() and data['id'] not in results_seen:
                                results.append(data)
                                results_seen.append(data['id'])

                # Searching via tags
                if text_tags != "":
                    text_tags = text_tags.split(",")
                    for tag in text_tags:
                        for data in cli_note_data['data']:
                            if tag.lower() in [each_tag.lower() for each_tag in data['tags']] and data['id'] not in results_seen:
                                results.append(data)
                                results_seen.append(data['id'])

                self.pretty_print({"data" : results})

# Add argument parser to handle params and options
if __name__ == "__main__":
    
    # Creating instance of class
    sv = cli_vault()

    # Argument parser to handle arguments for different subcli_notes and flags
    parser = argparse.ArgumentParser(prog='cli-vault', description="Store cli notes or other notes with our tool")
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "add, delete, list, or search"
    
    # Add cli_note setup
    parser_add = subparsers.add_parser('add', help='Allows you to add a cli note')
    parser_add.add_argument('-c', '--cli_note', metavar="<cli note>", help='Cli note to store')
    parser_add.add_argument('-d', '--description', metavar="<description>", help='A short description to recall note')
    parser_add.add_argument('-t', '--tags', metavar="<tags comma seperated>", help='Tags to associate cli note with')
    parser_add.set_defaults(func=sv.add)

    # Delete cli_note setup
    parser_delete = subparsers.add_parser('delete', help='Allows you to remote a cli note')
    parser_delete.add_argument('-id', '--cli_note_id', help='Id of cli note to delete', required=True)
    parser_delete.set_defaults(func=sv.delete)
    
    # List cli_note setup
    parser_list = subparsers.add_parser('list', help='Shows stored cli notes')
    parser_list.set_defaults(func=sv.list_cli_notes)

    # Search cli_note setup
    parser_search = subparsers.add_parser('search', help='Search for stored cli notes by text')
    parser_search.add_argument('-a', '--all', help='Search for text in all (cli note, description, and tags)')
    parser_search.add_argument('-c', '--cli_note', help='Search text by cli note')
    parser_search.add_argument('-d', '--description', help='Search text by description')
    parser_search.add_argument('-t', '--tags', help='Search by tags (comma separated)')
    parser_search.set_defaults(func=sv.search)

    # Update cli_note setup
    parser_update = subparsers.add_parser('update', help='Allows you to update a cli note')
    parser_update.add_argument('-id', '--cli_note_id', help='Id of cli note to update', required=True)
    parser_update.add_argument('-c', '--cli_note', metavar="<cli note>", help='Cli note to update')
    parser_update.add_argument('-d', '--description', metavar="<description>", help='Description to update')
    parser_update.add_argument('-t', '--tags', metavar="<tags comma separated>", help='Tags to update')
    parser_update.set_defaults(func=sv.update)

    # Running arg parser
    args = parser.parse_args()
    args.func(args)