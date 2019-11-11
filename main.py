import random as rd
from client import Client
from serveur import Serveur
import time
import threading
from datetime import datetime


def clients_thread(client_list):
    global clients_running
    global threads_alive
    print("Clients thread starting..\n")
    threads_alive += 1
    for client in client_list:
        file_attente.append(client)
    clients_running = False
    print("Clients thread finished..")
    threads_alive -= 1


def launch_serveurs(num=1):
    global threads_alive
    for i in range(num):
        server = threading.Thread(target=serveur_thread, args=(i + 1,))
        server.start()
        threads_alive += 1


def serveur_thread(num):
    global threads_alive
    global clients_running
    serveur = Serveur(num)
    print("Starting Serveur #" + str(num))
    while clients_running or len(file_attente) > 0:
        if len(file_attente) > 0:
            serveur.sert(file_attente.pop(0))
        else:
            time.sleep(0.5)
    print("Serveur #" + str(num) + " closing..")
    threads_alive -= 1


def main():
    global threads_alive
    global clients
    global clients_running

    # 50 clients
    for i in range(500):
        # charge de travail: au moins 3 matrices de jusqu'a 50X50 par client
        client = Client(i + 1, rd.randint(3, 50), 51, 51)
        clients.append(client)

    # parallel
    print("Execution en parallel")
    tstart = datetime.now()
    thread_clients = threading.Thread(target=clients_thread, args=(clients,))
    thread_clients.start()
    launch_serveurs(5)
    while threads_alive > 0:
        do_nothing = 0
    tend = datetime.now()
    delta_parallel = tend - tstart

    # seriel
    print("Execution seriel")
    clients_running = True
    tstart = datetime.now()
    thread_clients = threading.Thread(target=clients_thread, args=(clients,))
    thread_clients.start()
    launch_serveurs(1)
    while threads_alive > 0:
        do_nothing = 0
    tend = datetime.now()
    delta_seriel = tend - tstart
    print("temps d'execution seriel total: " + str(delta_seriel.total_seconds()) + " secondes")
    print("temps d'execution parallel total: " + str(delta_parallel.total_seconds()) + " secondes")


clients = []
threads_alive = 0
clients_running = True  # il y aura des clients..
file_attente = []
if __name__ == '__main__':
    main()
