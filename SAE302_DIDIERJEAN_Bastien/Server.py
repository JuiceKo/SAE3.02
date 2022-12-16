import os,psutil, platform, time, sys, logging, socket


class Server:
    def __init__(self, host: tuple):
        self.host = host
        self.killed = False

    def start(self):
        while not self.killed:
            self.server = socket.socket()
            print("Socket serveur créé")
            self.__bind(self.host)
            self.server.listen(1)

            message = ""
            while not self.killed and message != "reset":
                print("en attente d'un client")
                self.conn, self.address = self.server.accept()
                print(f"Un client avec l'addresse : {self.address} s'est connecté")

                message = ""
                while not self.killed and message != "reset" and message != "disconnect":
                    try:
                        message = self.conn.recv(1024)
                        #if not msgcl:
                            #break  # prevents infinite loop on disconnect
                    except ConnectionResetError:
                        break
                    else:
                        commande = message.decode()
                        print(f"Message du client: {commande}")
                        self.__gestionMessage(commande, self.address)

                print("Déconnexion du client...")
                self.conn.close()

            print("Fermeture du serveur...")
            self.server.close()

    def __gestionMessage(self, commande: str, addr: tuple):
        if commande == "kill":
            print("Le serveur va s'arrêter...")
            self.killed = True
        elif commande == "OS":
            reponse= (platform.system(), platform.release())
        elif commande == "Name":
            reponse =(socket.gethostname())
        elif commande == "CPU":
            reponse =('Le CPU est utilisé à :', psutil.cpu_percent(4), '%')
        elif commande == "RAM":
            reponse = ('Il y a', psutil.virtual_memory()[0] / 1000000000, ' GB de RAM au total,',
                  psutil.virtual_memory()[3] / 1000000000, 'GB de RAM utilisée et',
                  psutil.virtual_memory()[4] / 1000000000, 'GB de RAM libre.')
        elif commande == "IP":
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            print("Votre adresse ip est :", IPAddr)

        self.conn.send(reponse.encode())



    
    def __bind(self, host: tuple):
        while True:
            try:
                self.server.bind(host)
                logging.debug(f"Socket bound to {host}")
            except OSError:
                logging.info(f"Port {host[1]} not available. Retrying...")
                time.sleep(10)
                continue
            else:
                break
    
    def kill(self):
        try:
            self.client.send("kill".encode())
            self.client.close()
            self.server.close()
            self.killed = True
        except Exception:
            # Do not care about errors here, we're making sure the server is killed
            pass

if __name__ == "__main__":
    port = 10000
    host = "0.0.0.0"
    try:
        port = int(sys.argv[1])
    except:
        # Is is either a IndexError or a ValueError, default on port 10000 on both cases
        logging.warning(f"Invalid or no port given, using default port {port}...")



    server = Server((host, port))
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: killing server...")
        server.kill()
