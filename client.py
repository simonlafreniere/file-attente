import matrices as Matrices
import random as rd


class Client:
    def __init__(self, num=1, nbMatrices=2, max_lignes=6, max_colonnes=6):
        self.num = num
        self.matrices = {}
        for i in range(nbMatrices):
            if i == 0:
                m = Matrices.Matrice(rd.randint(1, max_lignes), rd.randint(1, max_colonnes))
            else:
                m = Matrices.Matrice(self.matrices[i - 1].colonnes, rd.randint(1, max_colonnes))
            m.randomFilling(-5, 15)
            self.matrices[i] = m
