# transterminal

<img src="/extras/trans_terminal.png" width=100 align="left">

transterminal is a utility that can be used to share a virtual terminal with anyone over the internet.  You run the `transterminal.py` Python script on a "server" machine, and "clients" can access the virtual terminal the server provides through a website hosted by a separate webserver.

Changes to one terminal are replicated on everyone else's terminals.  If one user types a character, everyone else sees what was typed.  If something is printed to the terminal, it shows up on everyone's terminal.

This was mainly written as a kind of proof of concept, so it doesn't have very many features, isn't really that secure, and could probably be optimised a bit.

## **huge warning**
this utility allows you to share access to your computer with *anyone* on the internet.  If transterminal is hosting a shell program like `bash` or `zsh`, anyone who can access your server can do anything they could if they were physically using a terminal on your computer.  Be very careful when exposing this server to the public internet.

## usage
the main `transterminal` server can be launched by running `python transterminal.py`.  you can pass arguments to the script to set a few options.  There are only three options at the minute (which are all optional), which are:

| argument      | default       | description                   |
|---------------|---------------|-------------------------------|
| `-h`          |               | print these options + usage   |
| `--ws_port`   | 5678          | specify the websocket port    |
| `[cmd]`       | `zsh`         | the command to host           |

The client webpage has to be hosted using a separate HTTP or HTTPS webserver.  When a client connects to the web server, they can specify their name, and give a user colour.  These are shown in the top right of every user's screen (it shows who is currently connected to the transterminal server).  You can also specify a custom Websocket port number or host url.

in theory, one person could host the transterminal server, and each client could locally host their own client webserver.  alternatively, one person can host both servers, which everyone connects to.

## technologies used
The main server program is a Python script that uses [Pexpect](https://github.com/pexpect/pexpect) to spawn and control a specified process.  The `stdout` of the process is sent using the [websockets](https://github.com/aaugustin/websockets) library, which is also used to receive data that is sent to the processes `stdin`.

The client side is written in vanilla JavaScript.  It uses the WebSockets API built into JavaScript.  The terminal is rendered using [Xterm.js](https://xtermjs.org/).

When a user types a character into the client terminal, the character is sent to the server and send to the `stdin` of the process.  This is echoed to the processes `stdout`, which is then sent to each of the users connected to the server.  The effect of this is that when a user types a character, it shows up on everyone's terminal.