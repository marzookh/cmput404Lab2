#!/usr/bin/env python3
from multiprocessing import Process
import socket, sys
import time
from urllib.request import proxy_bypass

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    proxy_host = 'www.google.com'
    proxy_port = 80
    #buffer_size = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            # create a new client socket to communicate with the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:

                remote_ip = get_remote_ip(proxy_host)
                proxy_socket.connect((remote_ip , proxy_port))
                print (f'Socket Connected to {proxy_host} on ip {remote_ip}')

                #recieve data, wait a bit, then send it back
                p = Process(target=handler,args=(conn,addr,proxy_socket))
                p.daemon = True
                p.start()

            conn.close()

def handler(conn,addr,proxy_socket):
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    proxy_socket.sendall(full_data)
    time.sleep(0.5)
    proxy_socket.shutdown(socket.SHUT_WR)
    data = proxy_socket.recv(BUFFER_SIZE)
    conn.send(data)

if __name__ == "__main__":
    main()
