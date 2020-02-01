# Othello_protocol

This project includes server and clients following the Othello_protocol

## Server

requirements: Python 3.7

To run the server.

```
python server/othello_game_server.py [port number]
```

## Library

Contain Python & C++

requirements: 
- Python 3.7
- C++17

If you want to see an example code, read lib/c++/othello.cpp or lib/python/othello.py

## Current Version & Patch Note

- **othello protocol v1.1 (2020.02.01)**
  - Time Limit Changed (20s -> 15s).
  - "Update" msg has *move* key value which represent lastest movement on board. (to see in detail, read server/msg.py)

## Previous Version List

- othello protocol v1.0 (2020.01.25)
  - Initial version.