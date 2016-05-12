from django.utils import timezone
from django.shortcuts import render
from laverie.models import Appareil


def index(request):
    appareils = Appareil.objects.all()
    nb_machines_libres = Appareil.objects.filter(type="machine", libre=True).count()
    nb_seche_linges_libres = Appareil.objects.filter(type="seche_linge", libre=True).count()
    for a in appareils:
        a.actualiser()
        a.save()
    return render(request, 'laverie/index.html', locals())


def lancer_decompte(request, id):
    print("Lancement du decompte " + str(id))
    appareil = Appareil.objects.get(id=id)
    print("Heure actuelle : " + str(timezone.now()))
    print("Duree de l'appareil : " + str(appareil.duree))
    appareil.heure_fin = timezone.now() + timezone.timedelta(minutes=appareil.duree)
    appareil.libre = False
    appareil.save()
    print("Heure de fin : " + str(appareil.heure_fin))
    appareil.actualiser()
    print("Temps restant : " + str(appareil.temps_restant))
    return index(request)


def corriger_decompte(request, id, valeur):
    appareil = Appareil.objects.get(id=id)
    appareil.heure_fin = timezone.now() + timezone.timedelta(minutes=int(valeur))
    appareil.actualiser()
    return index(request)


def interesse(request, id):
    appareil = Appareil.objects.get(id=id)
    appareil.add_interesse()
    return index(request)


def plus_interesse(request, id):
    appareil = Appareil.objects.get(id=id)
    appareil.remove_interesse()
    return index(request)

