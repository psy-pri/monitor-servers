import pickle
from CheckServer import Server

servers = pickle.load(open("servers.pickle","rb"))

for server in servers:
    server_up = 0
    for point in server.history:
        if point[1]:
            server_up += 1
    print("{} has been up {} \n Total History: {}".format(server.name,server_up / len (server.history) * 100,len(server.history)))