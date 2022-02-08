'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

'''

import os
import socket
import mimetypes
import subprocess
class HTTPServer:
    def __init__(self,host,port):
        socket_1= socket.socket()
        socket_1.bind((host,port))
        socket_1.listen()
        while True:
            print("Waiting for connection")
            (c,cip) = socket_1.accept()
            message=c.recv(1000).decode()
            # print(message)
            msgsplit=message.splitlines()
            # print(msgsplit[0])
            msg=msgsplit[0].split(" ")
            directorypath=msg[1]
            
            root=os.getcwd()
            filepath=directorypath.split("/")[-1]
            
            filenames1=os.listdir(os.path.join(root,"bin"))
            filenames2=os.listdir(os.path.join(root,"www"))
            #print("fffffffffffffffff",filenames2)

            datapath=root+directorypath
            #print("dddddddddddddd",datapath)
            
            if directorypath=="/www":
                head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
                for file in filenames2:
                    head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
                c.sendall(head.encode())

            elif directorypath=="/bin":
                head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
                for file in filenames1:
                    head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
                c.sendall(head.encode())

            elif os.path.isfile(datapath):
                if filepath in filenames2:
                    f=open(datapath,'rb')
                    result=f.read()
                    f.close()
                    res=f'HTTP/1.1 200 ok \n Content-Type={mimetypes.MimeTypes().guess_type(filepath)[0]}\n Content-Length:{len(str(result))}\n Connection:close\n\n'
                    res=res.encode()
                    res+=result
                    c.sendall(res)

                elif directorypath=='/bin/ls' :
                    res = os.popen('dir')
                    read=res.read()
                    data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
                    data=data.encode()
                    res=data+read.encode()
                    c.sendall(res)

                elif directorypath =="/bin/test.py":
                    process=subprocess.Popen(['python','D:\\computer systems\\comp sys 3\\ComputerSystems-p3\\bin\\test.py'], shell=False,stdout=subprocess.PIPE)
                    com = process.communicate()[0]
                    d=com.decode()
                    data= 'HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
                    data=data.encode()
                    res=data+d.encode()
                    c.sendall(res)

            else:
                data="HTTP/1.1 200 OK \n"
                data+="Content-Type: text/html \n"
                data+="Content-Length: " + str(1024) + "\n"
                data+="Connection:close\n"
                data+="\n"
                data+="<html><body><h1>Webserver under construction</h1></body></html>\n\n"
                c.send(data.encode())
        socket_1.close()

 
 
def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)
 
if __name__ == "__main__":
    main()