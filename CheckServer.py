import socket 
import ssl
from datetime import date, datetime
import pickle #save runtime info in a pickle file after py file execution 
import subprocess #helps with firewall connectivity issues in servers 
import platform #helps to know the platform like windows or linux
from EmailAlert import email_alert 

'''
This class represents a server

name: server name/ IP address 
port: server port to connect to
connection: type of connection - ssl,ping
priority: priority type - low,high 

history - stores history of server
alert - check flag to send alert only once in case the server is down
'''

class Server():
    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port 
        self.connection = connection.lower()
        self.priority = priority.lower()
        
        self.history = [] 
        self.alert = False 
    
    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

        try:
            if self.connection == "plain":
                socket.create_connection((self.name,self.port),timeout=10)
                msg = "{} is up, on port {}".format(self.name,self.port)
                success = True
                self.alert = False
            elif self.connection == "ssl":
                socket.create_connection((self.name,self.port), timeout=10)
                msg = "{} is up, on port {}".format(self.name,self.port)
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = "{} is up, on port {}".format(self.name,self.port)
                    success = True
                    self.alert = False
        except socket.timeout: #connection is not refused but is not established as well
            msg = "server: {} timeout, on port {}".format(self.name,self.port)
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = "server: {} {}".format(self.name,e)
        except Exception as e:
            msg = "No clue?? {}".format(e)
    
        if success == False and self.alert == False:
            #send alert
            self.alert = True
            email_alert(self.name,"{}\n{}".format(msg,now),"pri.test2103@gmail.com")
            
        self.create_history(msg,success,now)

    def create_history(self, msg, success, now):
        history_max  = 100
        self.history.append((msg,success,now))
        
        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' 
            if platform.system().lower() == "windows"
            else "c",self.name ), shell=True, universal_newlines=True)
            if "unreachable" in output:
                return False
            else:
                return True 
        except Exception:
            return False

if __name__ == "__main__":
    try:
        servers = pickle.load(open("servers.pickle","rb"))
    except:
        servers = [
            Server("google.com", 80, "plain", "high"),
            Server("smtp.gmail.com", 465, "ssl", "high"),
            Server("reddit.com", 80, "plain","high")]

    for server in servers:
        server.check_connection()
        print(len(server.history))
        print(server.history[-1])

    pickle.dump(servers, open("servers.pickle", "wb")) #pickle.dump(what u want to save, open(filename.pickle, write mode))