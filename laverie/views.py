from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from laverie.models import Appareil, Utilisation
from laverie.serializers import AppareilSerializer, UtilisationSerializer


def index(request):
    appareils = Appareil.objects.all()
    nb_machines_libres = Appareil.objects.filter(type="machine", libre=True).count()
    nb_seche_linges_libres = Appareil.objects.filter(type="seche_linge", libre=True).count()
    for a in appareils:
        a.actualiser()
        a.save()
    return render(request, 'laverie/index.html', locals())


def lancer_decompte(request, id):
    appareil = Appareil.objects.get(id=id)
    nouvelle_utilisation = Utilisation(appareil=appareil)
    nouvelle_utilisation.save()
    appareil.heure_fin = timezone.now() + timezone.timedelta(minutes=appareil.duree)
    appareil.libre = False
    appareil.save()
    appareil.actualiser()
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
    utilisations = []
    pourcentage_par_jour = []
    for utilisation in all_utilisations:
        utilisations.append(utilisation.date)
    for jour in range(7):
        pourcentage = len([u for u in utilisations if u.weekday() == jour])/total if total != 0 else 0
        pourcentage_par_jour.append(pourcentage)
    lundi = int(pourcentage_par_jour[0]*100)
    mardi = int(pourcentage_par_jour[1]*100)
    mercredi = int(pourcentage_par_jour[2]*100)
    jeudi = int(pourcentage_par_jour[3]*100)
    vendredi = int(pourcentage_par_jour[4]*100)
    samedi = int(pourcentage_par_jour[5]*100)
    dimanche = int(pourcentage_par_jour[6]*100)

    string_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    liste_de_liste_de_valeurs = []

    for jour in range(7):
        liste_de_valeurs = []
        for heure in range(12):
            liste_de_valeurs.append(len([u for u in utilisations
                                         if u.weekday() == jour and u.hour == 2*heure]))
        liste_de_liste_de_valeurs.append(liste_de_valeurs)

        valeurs_par_jour = zip(string_jours, liste_de_liste_de_valeurs)

    return render(request, 'laverie/statistiques.html', locals())


class AppareilList(APIView):

    def get(self, request):
        appareils = Appareil.objects.all()
        serializer = AppareilSerializer(appareils, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class UtilisationList(APIView):

    def get(self, request):
        utilisations = Utilisation.objects.all()
        serializer = UtilisationSerializer(utilisations, many=True)
        return Response(serializer.data)

    def post(self):
        pass


