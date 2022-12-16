#import socket
#import threading
#from socket import AF_INET, SOCK_STREAM
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QDialog, QMessageBox, QTabWidget, QVBoxLayout, QPlainTextEdit, QTextEdit, QTableWidget,QTableWidgetItem
import sys
#from threading import Thread




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        widget = QWidget()
        self.resize(500, 500)
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Invité de commande")

        self.__IP = QLabel("IP")
        self.__IPEdit = QLineEdit("localhost")
        self.__port = QLabel("Port")
        self.__portEdit = QLineEdit("10000")
        self.__start = QPushButton("Connexion au serveur")
        self.__envois = QLineEdit("")
        self.__envoisBoutton = QPushButton("Envoyer la commande")
        self.__recv = QTextEdit("")
        self.__recv.setReadOnly(True)
        self.__exit = QPushButton("Quitter")

        grid.addWidget(self.__IP, 0, 0)
        grid.addWidget(self.__IPEdit, 0, 1)
        grid.addWidget(self.__port, 1, 0)
        grid.addWidget(self.__portEdit, 1, 1)
        grid.addWidget(self.__start, 3, 0, 1, 2)
        grid.addWidget(self.__envois, 4, 0, 1, 2)
        grid.addWidget(self.__envoisBoutton, 5, 0, 1, 2)
        grid.addWidget(self.__recv, 6, 0, 1, 2)
        grid.addWidget(self.__exit, 7, 0, 1, 2)

        self.__start.clicked.connect(self._connexion)
        self.__envoisBoutton.clicked.connect(self.__envoit)
        self.__exit.clicked.connect(self.__quitter)



    def _connexion(self):
        self.__client_socket = socket.socket()
        addr = self.__IPEdit.text()
        port = int(self.__portEdit.text())
        try:
            self.__client_socket.connect((addr, port))
        except socket.error as err:
            if err.errno == 10061:
                print("Connection with {addr}:{port} refused".format(addr=addr, port=port))
            else:
                raise
        else:
            print("Connexion réussie ...")

        message = ""

    def __envoit(self):
        message = ""
        message = self.__envois.text()
        self.__client_socket.send(message.encode())
        print("Message envoyé")
        if message == "disconnect" or "reset":
            data=("Deconnexion du serveur")
            self.__recv.setText(data)



        data = self.__client_socket.recv(1024).decode()
        print(f"Message du serveur : {data}")
        self.__recv.setText(data)



    def __quitter(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()