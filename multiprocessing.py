from asyncio.subprocess import STDOUT
import multiprocessing
import os
import socket
import mimetypes
import subprocess
class HTTPServer:
    def __init__(self,host,port):
        self.host=host
        self.port=port

    def wwwdirectorypath(self,directorypath,filenames2,c):
        head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
        for file in filenames2:
            head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
        c.sendall(head.encode())

    def bin_directory_path(self,directorypath,filenames1,c):
        head = 'HTTP/1.1 200 OK \n Content-Type:text/html \n Content-Length:1024 \n Connection: close\n\n'
        for file in filenames1:
            head+=f'<a href="{os.path.join(directorypath,file)}">{file}</a><br>'
        c.sendall(head.encode())

    def given_file_in_www(self,datapath,filepath,c):
        f=open(datapath,'rb')
        result=f.read()
        f.close()
        res=f'HTTP/1.1 200 ok \n Content-Type={mimetypes.MimeTypes().guess_type(filepath)[0]}\n Content-Length:{len(str(result))}\n Connection:close\n\n'
        res=res.encode()
        res+=result
        c.sendall(res)

    def bin_ls(self,c):
        res = os.popen('dir')
        read=res.read()
        data= "HTTP/1.1 200 OK\nContent-Type: text/plain \n Content-Length: 1024\nConnection: Closed\n\n"
        data=data.encode()
        res=data+read.encode()
        c.sendall(res)

    def bin_test(self,c):
        process=subprocess.Popen(['python','D:\\computer systems\\comp sys 3\\ComputerSystems-p3\\bin\\test.py'], shell=False,stdout=subprocess.PIPE)
        com = process.communicate()[0]
        d=com.decode()
        data= 'HTTP/1.1 200 OK \n Content-Type:text/plain \n Content-Length:1024 \n Connection: close\n\n'
        data=data.encode()
        res=data+d.encode()
        c.sendall(res)

    def given_url_empty(self,c):
        data="HTTP/1.1 200 OK \n"
        data+="Content-Type: text/html \n"
        data+="Content-Length: " + str(1024) + "\n"
        data+="Connection:close\n"
        data+="\n"
        data+="<html><body><h1>Webserver under construction</h1></body></html>\n\n"
        c.send(data.encode())

    def execute(self):    
        socket_1= socket.socket()
        socket_1.bind((self.host,self.port))
        socket_1.listen()
        while True:
            print("Waiting for connection")
            (c,cip) = socket_1.accept()
            process = multiprocessing.Process(target=self.clienturl,args=(c, ))
            process.start()
            process.join()
    
    def clientcodeurl(self,c):
            message=c.recv(1000).decode()
            msgsplit=message.splitlines() 
            msg=msgsplit[0].split(" ")
            directorypath=msg[1]
            root=os.getcwd()
            filepath=directorypath.split("/")[-1]
            filenames1=os.listdir(os.path.join(root,"bin"))
            filenames2=os.listdir(os.path.join(root,"www"))

            datapath=root+directorypath

            if directorypath=="/www":
                self.wwwdirectorypath(directorypath,filenames2,c)

            elif directorypath=="/bin":
                self.bin_directory_path(directorypath,filenames1,c)

            elif os.path.isfile(datapath):
                if filepath in filenames2:
                    self.given_file_in_www(datapath,filepath,c)

                elif directorypath=='/bin/ls' :
                    self.bin_ls(c)

                elif directorypath=="/bin/test.py":
                    self.bin_test(c)
            
            elif ((directorypath!="/www") and (directorypath!="/bin")) :
                c.send("HTTP/1.1 404 not found".encode())

            else:
                self.given_url_empty(c)
 
 
def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    server = HTTPServer('127.0.0.1', 8888)
    server.execute()
 
if __name__ == "__main__":
    main()