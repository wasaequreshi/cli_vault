# What is it?

This tool helps developers improve productivity by managing commonly used commands and notes. 

# Why?

Sometimes we forget a command we used in the past. You can quickly store them with this tool in case you need to reference them again. You can store other information 
too such as ip addresses, api end points, links, and much more to recollect at a later time. 

Yes you can save this in a file or document but sometimes those can be misplaced or difficult to find.

# How to use
First run the following commands:

```sh
Install python3 on machine
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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

You'll be prompted via vim to input the cli note, description, and tags.

## Delete a cli note:

```sh
➜  ~ cli-vault list
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
➜  ~ cli-vault list 
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key"
        ]
    }
]
➜  ~ cli-vault update 83e9f9d1
```

You'll be prompted via vim to update the cli note, description, and tags.

## List all the cli notes stored:

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
➜  ~ cli-vault search -a my_private_key 
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -a into 
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]
```

### Cli Note:

This will only search for the terms on cli_note.

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -c unique 
No results :(
```

### Description:

This will only search for the terms on description.

```sh
➜  ~ cli-vault list 
[
    {
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
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
        "cli_note": "ssh -i my_private_key ubuntu@localhost",
        "description": "ssh into server with private key",
        "id": "83e9f9d1",
        "tags": [
            "ssh",
            "private key",
            "unique"
        ]
    }
]

➜  ~ cli-vault search -t into 
No results :(
```