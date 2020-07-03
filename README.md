# What is it?

This tool helps developers improve productivity by managing commonly used commands and notes. 

# How to use
```sh
python3 cli-vault.py add -c <command or note to store> -d <description of command or note, what, why, when etc> -t <tags such as "maintenance, release">
```

```sh
python3 cli-vault.py delete -id <command id>
```

```sh
python3 cli-vault.py list
```

Search doesn't work
```sh
python3 cli-vault.py search -t <text to search for  command>
```