import socket
import sys

rs_port=int(sys.argv[1]) #safe to cast port nums as int always? 
rs_dict = {}
ts1=""
ts2=""
ts1_hostname=""
ts2_hostname=""
outfile = open("rsresponses.txt", "w")

with open("rsdatabase.txt", "r") as infile:
    ts1, ts1_hostname = infile.readline().strip().split()
    ts2, ts2_hostname = infile.readline().strip().split()

    for line in infile: 
        info = line.strip().split()
        dname=info[0]
        ip=info[1]
        rs_dict[dname.lower()]=ip

rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rs_sock.bind(("",rs_port))

def decode_client(csockid, addr, msg):
    #msg = csockid.recv(1024).decode("utf-8")
    #msgLst = msg.strip().split()
    msgLst = msg.strip().split()
    dname = msgLst[1].lower()
    req_id= (int)(msgLst[2])
    flags = msgLst[3].lower()
    rs_response=""
    
    if dname.endswith(ts1) or dname.endswith(ts2):
        if flags == "it":  
            hostname = ts1_hostname if dname.endswith(ts1) else ts2_hostname #is hostname just  com and edu or the whole thing?
            rs_response = f"1 {dname} {hostname} {req_id} ns"
            csockid.sendall(rs_response.encode("utf-8"))
            # rs_query = f"0 {dname} {hostname} {req_id+1} it"
        else:
            rs_response=forward(msg)
            csockid.sendall(rs_response.encode("utf-8"))
            
    elif dname in rs_dict:
        rs_response = f"1 {dname} {rs_dict[dname]} {req_id} aa"  
        csockid.sendall(rs_response.encode("utf-8"))
    else:
        rs_response = f"1 {dname} 0.0.0.0 {req_id} nx"
        csockid.sendall(rs_response.encode("utf-8"))

    outfile.write(rs_response + "\n")
        
    csockid.close()

def forward(og_message):
    msgLst = og_message.strip().split()
    dname = msgLst[1].lower()
    req_id= (int)(msgLst[2])
    flags = msgLst[3].lower()
    server = ts1_hostname if dname.endswith(ts1) else ts2_hostname
    
    ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts_sock.connect((server, rs_port)) 
    ts_sock.send(f"0 {dname} {req_id} {flags}".encode("utf-8"))
    response = ts_sock.recv(1024).decode("utf-8")
    ts_sock.close()

    if response.endswith(" aa"):
        response = response.replace(" aa", " ra")

    return response

while True:
    rs_sock.listen(1)
    csockid, addr = rs_sock.accept()
    message = csockid.recv(1024).decode("utf-8")
    #print(message)
    if (message == "done"):
        ts1_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts1_sock.connect((ts1_hostname, rs_port)) 
        ts1_sock.send(message.encode("utf-8"))
        ts1_sock.close()
        ts2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts2_sock.connect((ts2_hostname, rs_port)) 
        ts2_sock.send(message.encode("utf-8"))
        ts2_sock.close()
        outfile.close()
        break
    decode_client(csockid, addr, message)
    

    

