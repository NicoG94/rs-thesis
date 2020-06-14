#!/usr/bin/env python3
# Code/Movie_Recommender/scripts2/D06_predict/Dockerfile
# https://realpython.com/python-sockets/

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            print("start")
            data = conn.recv(1024)
            if not data:
                print("NO DATA")
            #    break
            print(f"DATA: {data}")
            conn.sendall(data)
            print("END")

#df = pd.read_csv("gcp_data/rs_predictions/prepared_data.csv")
