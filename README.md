# What is it?

This tool helps developers improve productivity by managing commonly used commands and notes. 

# How to use
First run the following commands:
```sh
    chmod +x cli-vault.py
    mv cli-vault.py /usr/local/bin/cli-vault
```

Add a command or note:

```sh
    cli-vault add -c <command or note to store> -d <description of command or note, what, why, when etc> -t <tags such as "maintenance, release">
```

Delete a command or note:

```sh
    cli-vault delete -id <command id>
```

List all the commands or notes stored
```sh
    cli-vault list
```

Search for a command or note based on some text
Note: Search doesn't work
```sh
    cli-vault search -t <text to search for  command>
```