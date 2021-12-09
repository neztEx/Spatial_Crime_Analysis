# Crime Analysis App Backend

## Development architecture

### `server.py` This file sets up server and creates a sparkcontext.

### `query_builder.py` Apis are defined for the backend using flask framework in this file.

### `query_builder.py` sparkcontext created in server.py passed on in this file and spark queries are run in sqlcontext in this file

## Setting up development environment

Upgrade the python to python3 (https://levelup.gitconnected.com/a-guide-to-upgrade-your-python-to-3-9-44ccb3eae31a)

Run the following commands in the backend directory

### `pip3 install -r requirements.txt` To install all dependencies

Make sure no process is running at port 5432.

### ` python3 server.py` Runs the app in the development mode.

`The server will run at the port 5432 locally`
