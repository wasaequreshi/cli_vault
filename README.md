# What is it?

This tool helps developers improve productivity by managing commonly used commands and notes. 

# How to use

Add a command or note:

```sh
python3 cli-vault.py add -c <command or note to store> -d <description of command or note, what, why, when etc> -t <tags such as "maintenance, release">
```

Delete a command or note:

```sh
python3 cli-vault.py delete -id <command id>
```

List all the commands or notes stored
```sh
python3 cli-vault.py list
```

Search for a command or note based on some text
Note: Search doesn't work
```sh
python3 cli-vault.py search -t <text to search for  command>
```