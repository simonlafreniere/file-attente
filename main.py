import random as rd
from client import Client
from serveur import Serveur
import time
import threading
from datetime import datetime
import copy
import numpy as np


def clients_thread(client_list):
    global clients_running
    global threads_alive

    print("Clients thread starting..\n")
    threads_alive += 1

    # temps d'arrivee selon distribution exponentielle, plus ou moins
    lamb = 1 / 60  # 60 clients par minute
    x = np.linspace(0, 60, 50)
    y = ((lamb * np.exp(-lamb * x)) * 100).astype(int)  # valeurs 0 ou 1
    wait_condition = 1
    for client in client_list:
        while wait_condition > 0:
            wait_condition = y[rd.randint(0, 50)]
            time.sleep(1)
        client.t_attente_start = datetime.now()
        file_attente.append(client)
        time.sleep(1)
    clients_running = False
    print("Clients thread finished..")
    threads_alive -= 1


def launch_serveurs(num=1, name="-"):
    global threads_alive

    for i in range(num):
        server = threading.Thread(target=serveur_thread, args=(i + 1, name,))
        server.start()
        threads_alive += 1


def serveur_thread(num, name):
    global threads_alive
    global clients_running

    serveur = Serveur(num, name)
    print("Starting Serveur #" + str(num))
    while clients_running or len(file_attente) > 0:
        if len(file_attente) > 0:
            client = file_attente.pop(0)
            client.t_attente_end = datetime.now()
            serveur.sert(client)
        else:
            time.sleep(0.1)
    print("Serveur #" + str(num) + " closing..")
    threads_alive -= 1


def main():
    global threads_alive
    global clients_running

    # 50 clients
    clients_seriel = []
    clients_parralel = []
    for i in range(50):
        # charge de travail: au moins 3 matrices de jusqu'a 8X8 par client
        client = Client(i + 1, rd.randint(3, 8), 9, 9)
        clients_seriel.append(client)
        clients_parralel.append(copy.deepcopy(client))

    # parallel
    print("Execution en parallel")
    tstart = datetime.now()
    thread_clients = threading.Thread(target=clients_thread, args=(clients_parralel,))
    thread_clients.start()
    launch_serveurs(2, "parallel")
    while threads_alive > 0:
        do_nothing = 0
    tend = datetime.now()
    delta_parallel = tend - tstart

    # seriel
    print("\n\nExecution seriel")
    clients_running = True
    tstart = datetime.now()
    thread_clients = threading.Thread(target=clients_thread, args=(clients_seriel,))
    thread_clients.start()
    launch_serveurs(1, "seriel")
    while threads_alive > 0:
        do_nothing = 0
    tend = datetime.now()
    delta_seriel = tend - tstart
    print("temps d'execution seriel total: " + str(delta_seriel.total_seconds()) + " secondes")
    temps_attente_moyen = 0
    for client_s in clients_seriel:
        temps_attente_moyen += client_s.get_temps_attente()
    temps_attente_moyen = temps_attente_moyen / len(clients_seriel)
    print("Temps d'attente moyen (seriel): " + str(temps_attente_moyen) + "secondes\n")

    print("temps d'execution parallel total: " + str(delta_parallel.total_seconds()) + " secondes")
    temps_attente_moyen = 0
    for client_p in clients_parralel:
        temps_attente_moyen += client_p.get_temps_attente()
    temps_attente_moyen = temps_attente_moyen / len(clients_parralel)
    print("Temps d'attente moyen (parallel): " + str(temps_attente_moyen) + " secondes")


threads_alive = 0
clients_running = True  # il y aura des clients..
file_attente = []
if __name__ == '__main__':
    main()
