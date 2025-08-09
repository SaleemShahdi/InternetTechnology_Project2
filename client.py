import socket
import sys

rs_hostname = sys.argv[1]
rs_port = int(sys.argv[2])

with open("hostnames.txt", "r") as infile:
    queries = [line.strip().split() for line in infile]

q_id = 1
resolved=[]

for query in queries:
    dname=query[0]
    flag=query[1]
    c_req = f"0 {dname} {q_id} {flag}"

    rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rs_sock.connect((rs_hostname, rs_port))
    #print(c_req)
    rs_sock.send(c_req.encode("utf-8"))

    response = rs_sock.recv(1024).decode("utf-8")
    rs_sock.close()

    info = response.strip().split()
    #print(info)

    resp_dname = info[1]   
    resp_ip = info[2]     
    resp_id = info[3]        
    resp_flag = info[4] 
        
    if resp_flag == "ns":
        resolved.append(response)
        q_id = q_id + 1
        ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts_sock.connect((resp_ip, rs_port))
        ts_query = f"0 {resp_dname} {q_id} {flag}"
        ts_sock.send(ts_query.encode("utf-8"))

        ts_response = ts_sock.recv(1024).decode("utf-8")
        ts_sock.close()
        
        resolved.append(ts_response)
    else:
        resolved.append(response)
    q_id = q_id + 1
    
    
rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rs_sock.connect((rs_hostname, rs_port))
rs_sock.send("done".encode("utf-8"))
rs_sock.close()
    
with open("resolved.txt", "w") as outfile:
    for i in resolved:
        outfile.write(i + "\n")

