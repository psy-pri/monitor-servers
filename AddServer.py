'''
This functionality is created to add a new server to the pickle file without deleting wit
'''

import pickle 
from CheckServer import Server

servers = pickle.load(open("servers.pickle","rb"))

print("Add server")

server_name = input("Enter server name ")
port = input("Enter port number ")
connection = input("Enter connection type: plain/ssl/ping ")
priority = input("Enter priority: high/low ")

new_server = Server(server_name, port, connection, priority)
servers.append(new_server)

pickle.dump(servers, open("servers.pickle", "wb"))
