from threading import Thread
import time
from django.shortcuts import render
from laverie.models import Appareil


class Compteur(Thread):
    def __init__(self, id, valeur):
        Thread.__init__(self)
        self.id = id
        self.valeur = valeur
        appareil = Appareil.objects.get(id=id)
        appareil.temps_restant = valeur
        appareil.save()
        print("Temps restant apres creation : " + str(appareil.temps_restant))

    def run(self):
        appareil = Appareil.objects.get(id=self.id)
        print("laul on lance un compteur")
        print(appareil.compteur_actif)
        print(appareil.temps_restant > 0)
        while appareil.compteur_actif and appareil.temps_restant > 0:
                appareil.temps_restant -= 1
                appareil.save()
                time.sleep(1)
                print(self.__str__() + " " + str(appareil.temps_restant) + " id : " + str(self.id))
                appareil = Appareil.objects.get(id=self.id)


compteurs = []
for j in range(1, Appareil.objects.all().count()+1):
    print("laul")
    compteurs.append(Compteur(j,0))
for compteur in compteurs:
    print("CECI EST UN COMPTEUR")
    compteur.start()


def index(request):
    print("laul index")
    appareils = Appareil.objects.all()
    nb_machines_libres = Appareil.objects.filter(type="machine", libre=True).count();
    nb_seche_linges_libres = Appareil.objects.filter(type="seche_linge", libre=True).count();
    return render(request, 'laverie/index.html', locals())


def lancer_decompte(request, id):
    print("laul lancer_decompte id " + str(id))
    appareil = Appareil.objects.get(id=id)
    appareil.temps_restant = appareil.temps_max
    appareil.save()
    print("Temps restant de l'id " + str(appareil.id) + " : " + str(appareil.temps_restant))
    appareil.libre = False
    appareil.compteur_actif = True
    appareil.save()
    print("Taille de la liste : " + str(len(compteurs)))
    print("Index appelé : " + id)
    appareil.temps_restant = appareil.temps_max
    appareil.save()
    compteurs[int(id)-1].join()
    compteurs[int(id)-1] = Compteur(id, appareil.temps_max)
    compteurs[int(id)-1].start()
    return index(request)


def corriger_decompte(request, id, valeur):
    print("On corrige l'id " + str(id))
    appareil = Appareil.objects.get(id=id)
    appareil.compteur_actif = False
    time.sleep(1.1)
    appareil.save()
    print("Compteur actif ? : " + str(appareil.compteur_actif))
    print("Thread associé ? " + str(compteurs[int(id)-1]))
    appareil.compteur_actif = True
    appareil.temps_restant = int(valeur)
    appareil.libre = valeur == 0
    compteurs[int(id) - 1] = Compteur(id, int(valeur))
    compteurs[int(id) - 1].start()
    appareil.temps_restant = int(valeur)
    appareil.save()
    return index(request)


def interesse(request, id):
    appareil = Appareil.objects.get(id=id)
    appareil.interesses += 1
    appareil.save()
    return index(request)


def plus_interesse(request, id):
    appareil = Appareil.objects.get(id=id)
    appareil.interesses -= 1
    appareil.save()
    return index(request)

