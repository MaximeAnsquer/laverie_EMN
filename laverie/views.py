from django.utils import timezone
from django.shortcuts import render
from laverie.models import Appareil, Utilisation


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
    nouvelle_utilisation = Utilisation(appareil=appareil)
    nouvelle_utilisation.save()
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
    print("Correction de " + str(id))
    appareil = Appareil.objects.get(id=id)
    print("Heure de fin valait " + str(appareil.heure_fin))
    appareil.heure_fin = timezone.now() + timezone.timedelta(minutes=int(valeur))
    appareil.save()
    appareil.actualiser()
    print("Heure de fin vaut maintenant " + str(appareil.heure_fin))
    return index(request)


def interesse(request, id):
    appareil = Appareil.objects.get(id=id)
    appareil.add_interesse()
    return index(request)


def plus_interesse(request, id):
    appareil = Appareil.objects.get(id=id)
    appareil.remove_interesse()
    return index(request)


def statistiques(request):
    all_utilisations = Utilisation.objects.all()
    total = all_utilisations.count()
    jours_utilisations = []
    pourcentage_par_jour = []
    for utilisation in all_utilisations:
        jours_utilisations.append(utilisation.date.weekday())
    for jour in range(7):
        pourcentage = len([j for j in jours_utilisations if j == jour])/total
        pourcentage_par_jour.append(pourcentage)
    lundi = pourcentage_par_jour[0]*100
    mardi = pourcentage_par_jour[1]*100
    mercredi = pourcentage_par_jour[2]*100
    jeudi = pourcentage_par_jour[3]*100
    vendredi = pourcentage_par_jour[4]*100
    samedi = pourcentage_par_jour[5]*100
    dimanche = pourcentage_par_jour[6]*100
    return render(request, 'laverie/statistiques.html', locals())

