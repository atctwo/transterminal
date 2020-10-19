import argparse
import transserver

print("transterminal!")

parser = argparse.ArgumentParser()
parser.add_argument("cmd", nargs="?", help="the program to run in the virtual terminal", default="zsh")
parser.add_argument("--http_port", metavar="hp", help="the port to run the http server under", default=8000, type=int)
parser.add_argument("--ws_port", metavar="wp", help="the port the run the WebSockets server under", default=5678, type=int)

args = parser.parse_args()

server = transserver.transterminal(args.cmd)
server.go()