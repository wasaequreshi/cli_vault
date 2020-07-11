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

    # pretty print results from list and search
    def pretty_print(self, cli_note_data):
        formatted_json = json.dumps(cli_note_data['data'], indent=4, sort_keys=True)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)

    # Open up editor to add/update notes
    def vim_editor(self, current):
        initial_message = current
        tf = tempfile.NamedTemporaryFile('w+', suffix=".tmp", delete=False)
        tf.write('\n'.join(initial_message))
        tf.close()

        call(['vim', tf.name])

        tf = open(tf.name, 'r')
        edited_message = tf.readlines()
        edited_message = [e_message.strip("\n") for e_message in edited_message]

        tf.close()

        os.unlink(tf.name)

        return edited_message

    # Processes input before passing to editor
    def vim(self, cli_note, description, tags):
        cli_note = self.vim_editor(["<cli note>"] if cli_note == [""] else cli_note)
        description = self.vim_editor(["<description>"] if description == [""] else description)
        tags = self.vim_editor(["<tags comma separated when passing via cli. If in vim, enter additional tags on new line>"] if tags == [""] else tags)

        return cli_note, description, tags

    # get all words to check and lower them
    def lower_words(self, data):
        all_words = ""
        
        # loop through each word
        for each_data in data:
            # If spaces, split at those and add indepedently
            each_data = each_data.split(" ")
            for word in each_data:
                all_words += word.lower()
        return all_words

    # Checking if multiple search in are passed to do an or and check what the boolean val would be
    def search_in_helper(self, word, search_in, data):
        result = False

        for si in search_in:
            result = result or (word.lower() in self.lower_words(data[si]))
        
        return result

    # search helper to search for text based on cli_note, description, tags, or all
    def search_helper(self, text, search_in, cli_note_data, results, results_seen):

        text = text.split(" ")
        for word in text:
            for data in cli_note_data['data']: 
                if self.search_in_helper(word, search_in, data) and data['id'] not in results_seen:
                    results.append(data)
                    results_seen.append(data['id'])

        return results, results_seen

    # cli_note to add
    def add(self, args):
        # Getting arguments
        cli_note = args.cli_note if args.cli_note else ""
        description = args.description if args.description else ""
        tags = args.tags if args.tags else ""

        # If it isn't blank, split at new line
        cli_note = cli_note.split("\\n")

        # If it isn't blank, split at new line
        description = description.split("\\n") 

        # If it isn't blank, split at comma, this stays the same
        tags = tags.split(",")
        
        # If all blank, open vim for each
        if cli_note == [""]:
            cli_note, description, tags = self.vim(cli_note, description, tags)
        
        # Need to check this each time, file could be corrupt which can cause program to crash
        if self.is_valid_file_path():
            # Loading data
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                unique_id = str(uuid.uuid4())[:8]
                # Creating new data
                new_data = {"id" : unique_id, "cli_note" : cli_note, "description" : description, "tags" : tags}
                
                # Appending to loaded data
                cli_note_data['data'].append(new_data)

                # Writing back to file
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)

                print(unique_id + " created")

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
                    print(cli_note_id + " deleted")
                else:
                    print("Invalid id: " + cli_note_id)
    
    # Updating stored cli_note
    def update(self, args):
        # Getting arguments
        cli_note = args.cli_note
        description = args.description
        tags = args.tags
        cli_note_id = args.cli_note_id

        # If it isn't blank, split at new line
        if cli_note != None:
            cli_note = cli_note.split("\\n")

        # If it isn't blank, split at new line
        if description != None:
            description = description.split("\\n") 

        # If it isn't blank, split at new line
        if tags != None:
            tags = tags.split(",")

        if cli_note == None and description == None and tags == None:
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                # Checking which data to update
                for data in cli_note_data['data']:
                    if data['id'] == cli_note_id:
                        cli_note, description, tags = self.vim(data['cli_note'], data['description'], data['tags'])

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
                            data['tags'] = tags
                        id_found = True
                #Write back to file
                with open(self.sv_cli_note_file_path, 'w') as outfile:
                    json.dump(cli_note_data, outfile, indent=4)

                # Print if it was updated or not
                if id_found:
                    print(cli_note_id + " updated")
                else:
                    print("Invalid id: " + cli_note_id)

    # Similar to ls, shows all the cli_notes stored
    def _list_cli_notes(self, args):
        # Just loading the file
        if self.is_valid_file_path():
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                return cli_note_data

    # separated into two functions to test results
    def list_cli_notes(self, args):
        
        cli_note_data = self._list_cli_notes(args)

        if len(cli_note_data['data']) == 0:
            print("No results :(")
        else:
            # Doing a json pretty print
            self.pretty_print(cli_note_data)

    # Searching for cli_notes
    def _search(self, args):
        # Getting arguments 
        text_all = args.a
        text_cli_note = args.c
        text_description = args.d
        text_tags = args.t
        text = args.text
        
        # No need to search for other flags
        if text_all:
            text_cli_note = False
            text_description = False
            text_tags = False
        
        # If no flags passed, will search through all
        if not (text_all or text_cli_note or text_description or text_tags):
            text_all = True
            print("No flags passed, searching through all.")
        
        # Loading file
        if self.is_valid_file_path():
            cli_note_data = {}
            with open(self.sv_cli_note_file_path) as json_file:
                cli_note_data = json.load(json_file)
                
                results_seen = []
                results = []
                # Searching all
                if text_all:
                    results, results_seen = self.search_helper(text, ['cli_note', 'description', 'tags'], cli_note_data, results, results_seen)

                # Searching via cli_note
                if text_cli_note:
                    results, results_seen = self.search_helper(text, ['cli_note'], cli_note_data, results, results_seen)
                
                # Searching via description
                if text_description:
                    results, results_seen = self.search_helper(text, ['description'], cli_note_data, results, results_seen)

                # Searching via tags
                if text_tags:
                    results, results_seen = self.search_helper(text, ['tags'], cli_note_data, results, results_seen)

                return results

    # separated into two functions to test results
    def search(self, args):
        results = self._search(args)

         # Printing proper message
        if len(results) == 0:
            print("No results :(")
        else:
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
    parser_add.add_argument('-t', '--tags', metavar="<tags comma separated when passing via cli>", help='Tags to associate cli note with')
    parser_add.set_defaults(func=sv.add)

    # Delete cli_note setup
    parser_delete = subparsers.add_parser('delete', help='Allows you to remote a cli note')
    parser_delete.add_argument('cli_note_id', help='Id of cli note to delete')
    parser_delete.set_defaults(func=sv.delete)
    
    # List cli_note setup
    parser_list = subparsers.add_parser('list', help='Shows stored cli notes')
    parser_list.set_defaults(func=sv.list_cli_notes)

    # Search cli_note setup
    parser_search = subparsers.add_parser('search', help='Search for stored cli notes by text')
    parser_search.add_argument('text', help='Id of cli note to update. With no flags, it will search through all')
    parser_search.add_argument('-a', action='store_true', help='Search for text in all (cli note, description, and tags)')
    parser_search.add_argument('-c', action='store_true', help='Search text by cli note')
    parser_search.add_argument('-d', action='store_true', help='Search text by description')
    parser_search.add_argument('-t', action='store_true', help='Search by tags (comma separated when passing via cli)')
    parser_search.set_defaults(func=sv.search)

    # Update cli_note setup
    parser_update = subparsers.add_parser('update', help='Allows you to update a cli note')
    parser_update.add_argument('cli_note_id', help='Id of cli note to update')
    parser_update.add_argument('-c', '--cli_note', metavar="<cli note>", help='Cli note to update')
    parser_update.add_argument('-d', '--description', metavar="<description>", help='Description to update')
    parser_update.add_argument('-t', '--tags', metavar="<tags comma separated when passing via cli>", help='Tags to update')
    parser_update.set_defaults(func=sv.update)

    # Running arg parser
    args = parser.parse_args()
    args.func(args)