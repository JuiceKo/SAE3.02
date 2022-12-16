import socket, platform, psutil, subprocess, sys




def Serveur():
    host = "0.0.0.0"
    port = 11000
    message = ""
    conn = None
    server_socket = None

    while message != "kill" :
        message = ""
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(1)
        
        print('En attente de connexion client ...')

        while message != "kill" and message != "reset":
            message = ""
            try :
                conn, addr = server_socket.accept()
                print(f"Client connecté depuis {addr}")

            except ConnectionError:
                print ("La connexion à échoué...")
                break
            else :
                while message != "disconnect" and message != "reset" and message != "kill":
                    reception = conn.recv(1024)
                    message = reception.decode()
                    print ("Message du client : ", message)


                    if message == 'OS':
                        reply = f" {platform.system()}, {platform.release()}"
                        conn.send(reply.encode())

                    elif message == 'info':
                        hostname = socket.gethostname()
                        IPAddr = socket.gethostbyname(hostname)
                        reply = (f"IP : {IPAddr} / Hostname : {hostname}" )
                        conn.send(reply.encode())


                    elif message == 'CPU':
                        reply = f" Le CPU est utilisé à {psutil.cpu_percent(4)} %"
                        conn.send(reply.encode())


                    elif message == 'RAM':
                        reply = f"Il y a {psutil.virtual_memory()[0] / 1000000000} GB de RAM au total, {psutil.virtual_memory()[3] / 1000000000} GB de RAM utilisée et {psutil.virtual_memory()[4] / 1000000000} GB de RAM libre"
                        conn.send(reply.encode())


                    elif message == 'IP':
                        hostname = socket.gethostname()
                        IPAddr = socket.gethostbyname(hostname)
                        reply = (f"Votre adresse ip est : {IPAddr}")
                        conn.send(reply.encode())


                    elif message == 'Name':
                        reply = socket.gethostname()
                        conn.send(reply.encode())


                    elif message[0:4] == 'DOS:':
                        if sys.platform == "win32":
                            p = message.split(':')
                            commande = p[1]
                            pipe = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 encoding='cp850', shell=True)

                            reply = f"résultat commande : \n {pipe.stdout.read()} {pipe.stderr.read()}"
                            conn.send(reply.encode())
                        else:
                            reply = f"Cette commande est impossible sur un système différent de Windows"
                            conn.send(reply.encode())


                    elif message[0:6] == 'Linux:':
                        if sys.platform.startswith("linux"):
                            p = message.split(':')
                            commande = p[1]
                            pipe = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 encoding='cp850', shell=True)

                            reply = f"résultat commande : \n {pipe.stdout.read()} {pipe.stderr.read()}"
                            conn.send(reply.encode())
                        else:
                            reply = f"Cette commande est impossible sur un système différent de Linux"
                            conn.send(reply.encode())

                    elif message[0:11] == 'Powershell:':
                        if sys.platform == "win32":
                            p = message.split(':')
                            commande = p[1]
                            p = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 encoding='cp850', shell=True)

                            reply = f"résultat commande : \n {p.stdout.read()} {p.stderr.read()}"
                            conn.send(reply.encode())
                        else:
                            reply = f"Cette commande est impossible sur un système différent de Windows"
                            conn.send(reply.encode())

                    elif message[0:6] == 'Shell:':
                        p = message.split(':')
                        commande = p[1]
                        pipe = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                encoding='cp850', shell=True)

                        reply = f"résultat commande : \n {pipe.stdout.read()} {pipe.stderr.read()}"
                        conn.send(reply.encode())



                    elif message == "reset":
                        reply = ""
                        conn.send(reply.encode())

                    elif message == "kill":
                        reply = " "
                        conn.send(reply.encode())

                    elif message == "disconnect":
                        reply = " "
                        conn.send(reply.encode())


                    else :
                        reply = "Commande non reconnu par le système"
                        conn.send(reply.encode())

                reply = f"Vous allez être déconnecté du serveur... "
                conn.send(reply.encode())
                conn.close()
                print ("Connexion rompue... ")

        server_socket.close()
        print ("Serveur fermé ...")


if __name__ == '__main__':
    Serveur()