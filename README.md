# CLI Vault

[![Build Status](https://api.travis-ci.org/wasaequreshi/cli_vault.svg?branch=master)](https://travis-ci.org/wasaequreshi/cli_vault)


# What is it?

This tool helps developers improve productivity by managing commonly used commands and notes on the cli. 

# Why?

Developers store scripts and other notes in an a wide array of different places such as Google Docs, Notes, Google Keep etc. Sometimes we misplace them or have a hard time recollecting our notes. 

cli-vault allows you to manage scripts and other notes via the cli. Developers can add, delete, update, list and search scripts and notes right from the cli. cli-vault is aimed to store cli related activity so you can quickly get what you need in your current session.  

This isn't just limited to cli activity. You can also store other developer information such as css syntax/notes, api endpoints, ip ranges, and other types of documentation.

# How to use
First run the following commands:

Make sure you have python3 installed on the machine

```sh
pip3 install -r requirements.txt
chmod +x src/cli_vault.py
cp src/cli_vault.py /usr/local/bin/cli-vault
```

## Add a cli note:

### via cli

```sh
➜  ~ cli-vault add -c "ssh -i my_private_key ubuntu@localhost" -d "ssh into server with private key" -t "ssh,private key"
9e9e5793 created
➜  ~ cli-vault list
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "9e9e5793",
        "tags": [
            "ssh",
            "private key"
        ]
    }
]
```

### via vim

```sh
➜  ~ cli-vault add
```

You will be prompted in vim to add a cli note.

```sh
<cli note>
~
~
~
...
:
```

Press "esc" and type ":wq" to save and quit. You will then be prompted to add a description in vim.

```sh
<description>
~
~
~
...
:
```

Press "esc" and type ":wq" to save and quit. You will finally be prompted to tags in vim.

```sh
<tags comma separated when passing via cli. If in vim, enter additional tags on new line>
~
~
~
...
:
```

Once completed, it should create a cli note.

```sh
➜  ~ cli-vault add
9e9e5793 created
```

## Delete a cli note:

```sh
➜  ~ cli-vault list
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "9e9e5793",
        "tags": [
            "ssh",
            "private key"
        ]
    }
]

➜  ~ cli-vault delete 9e9e5793 
9e9e5793 deleted
➜  ~ cli-vault list 
No results :(
```

## Update a cli note:

### via cli
```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key"
        ]
    }
]

➜  ~ cli-vault update 83e9f9d1 -c "ssh -i my_private_key ubuntu@remotehost" -d "ssh into remote server with private key" -t "ssh,private key,remote"
83e9f9d1 updated
➜  ~ cli-vault list 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "remote"
        ]
    }
]
```

### via vim

```sh
➜  ~ cli-vault update 83e9f9d1
```

You will be prompted in vim to update a cli note.

```sh
ssh -i my_private_key ubuntu@localhost
~
~
~
...
:
```

Press "esc" and type ":wq" to save and quit. You will then be prompted to update a description in vim.

```sh
ssh into server with private key
~
~
~
...
:
```

Press "esc" and type ":wq" to save and quit. You will finally be prompted to update tags in vim.

```sh
ssh
private key
remote
~
~
~
...
:
```

Once completed, it should update the cli note.

```sh
➜  ~ cli-vault update
83e9f9d1 updated
```

## List all the cli notes stored:

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key"
        ]
    }
]
```

## Search for notes via cli note, description, tags, or all

This allows you to search a text individually on cli note, description, and tags or search through all of them. 

### All:

This is searching for 'into' and 'unique' in cli note, description, and tags.

```sh
➜  ~ cli-vault search my_private_key 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search into 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -a unique 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]
```

By default, if no flags are passed, it will search all. In the last example the -a is unnecessary.

### Cli Note:

This will only search for the terms on cli notes.

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -c my_private_key
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search unique -c 
No results :(
```

### Description:

This will only search for the terms on description.

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -d into 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -d unique
No results :(
```

### Tags:

This will only search for the terms on tags.

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -t unique
[
    {
        "cli_note": [
            "ssh -i my_private_key ubuntu@localhost",
        ]
        "description": [
            "ssh into server with private key",
        ]
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search into -t 
No results :(
```