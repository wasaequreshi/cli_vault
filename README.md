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

# Examples

Add

```sh
cli-vault add -c "ssh -i mc.pem ubuntu@52.24.168.10" -d "ssh into minecraft server" -t "minecraft,server"
```

List

```sh
wqureshi:  cli-vault list
[
    {
        "command": "ssh -i mc.pem ubuntu@52.24.168.10",
        "description": "ssh into minecraft server",
        "id": "4258ab81",
        "tags": [
            "minecraft",
            "server"
        ]
    }
]
```

Delete

```sh
wqureshi: cli-vault delete -id "4258ab81" 
Command deleted
```

Search

```sh
wqureshi: cli-vault search  -c "what i use to ssh"
[
    {
        "command": "ssh -i mc.pem ubuntu@52.24.168.12",
        "description": "ssh into minecraft server",
        "id": "67a9a224",
        "tags": [
            "minecraft",
            "server"
        ]
    }
]
```

```sh
wqureshi: cli-vault search  -c "what i use for"
[]
```
In this example we can see that those words aren't found in any of the commands stored, so it returns blank