import matrices as Matrices
from datetime import datetime
import time


class Serveur:
    def __init__(self, num=1):
        self.num = num
        self.client_served = 0
        self.temps_service_total = 0
        self.temps_service_moyen = 0

    def sert(self, client):
        print("Serveur #" + str(self.num) + "\nService en cours pour Client #" + str(client.num) + "\n")
        tstart = datetime.now()
        result = Matrices.MultiplieXMatrices(client.matrices)
        tend = datetime.now()
        self.client_served += 1
        print("Resultat:\n" + str(result))
        delta = tend - tstart
        temps_service = delta.total_seconds()
        self.temps_service_total += temps_service
        self.temps_service_moyen = self.temps_service_total / self.client_served
        print("Temps de service: " + str(temps_service) + " secondes..")
        print("Temps de service moyen: " + str(self.temps_service_moyen) + " secondes..")
