import socket
from sys import argv

def findDomain(domainName, database):
    domainaddress = []
    for key, value in database.items():
        if key.lower() == domainName.lower():
            domainaddress.append(key)
            domainaddress.append(value)
            break
    return domainaddress

temp = []
with open("ts1database.txt", "r") as infile:
    for line in infile:
        broken = line.split()
        temp.append(broken)
database = dict(temp)
outfile = open("ts1responses.txt", "w")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(argv[1])
binding = ('', port)
s.bind(binding)
while True:
    s.listen(1)
    clientsocket, clientaddress = s.accept()
    message = clientsocket.recv(1024).decode("utf-8")
    #print(message)
    if (message == "done"):
        break
    message = message.split()
    domainName = message[1]
    newMessage = ""
    domainaddress = findDomain(domainName, database)
    #print(domainaddress)
    if (not (not(domainaddress))):
        newMessage = f"1 {domainaddress[0]} {domainaddress[1]} {message[2]} aa"
    else:
        newMessage = f"1 {domainName} 0.0.0.0 {message[2]} nx"
    #print(newMessage)
    clientsocket.send(newMessage.encode("utf-8"))
    outfile.write(newMessage+"\n")
    clientsocket.close()

outfile.close()
s.close()


