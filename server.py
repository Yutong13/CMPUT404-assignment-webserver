#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.data = self.data.decode('utf-8').lower()
        lines = self.data.split("\\n")
        self.data = lines[0].split(" ")
        self.data[1] = self.data[1].replace("../", '')

        if self.data[0] != "get":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Found\n\n", 'utf-8'))
            return
        
        if self.data[1][-1]== "/":
            try:
                with open("www/{}index.html".format(self.data[1]), "r") as webpage:
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\ncontent-type: text/html\n\n{}".format(webpage.read()), 'utf-8'))
                return

            except FileNotFoundError as e:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n", 'utf-8'))
                print(e)
                return
            except Exception as e:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n", 'utf-8'))
                print(e)
                return
                
        try: 
            request = self.data[1]
            with open("www{}".format(request), "r") as webpage:
                if ".html" in self.data[1]:
                    type = "html"
                elif ".css" in self.data[1]:
                    type = "css"
                else:
                    type = ""
                self.request.sendall(bytearray("HTTP/1.1 200 OK\ncontent-type: text/{}\n\n{}".format(type, webpage.read()),'utf-8'))
            return

        except FileNotFoundError as e:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n", 'utf-8'))
            print(e)
            return
        except IsADirectoryError as e2:
            print(e2)
            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\nLocation:http://{}:8080{}/\n\n".format(self.client_address[0], request), 'utf-8'))
            return

        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n", 'utf-8'))
        
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
