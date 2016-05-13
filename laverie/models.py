from django.utils import timezone
from django.db import models


class Appareil(models.Model):
    duree = models.IntegerField(default=50)
    heure_fin = models.DateTimeField(default=timezone.now)
    temps_restant = models.DurationField(default=timezone.timedelta(),null=True)
    interesses = models.IntegerField(default=0)
    libre = models.BooleanField(default=True)
    TYPES = (
        ('machine', 'Machine à laver'),
        ('seche_linge', 'Sèche linge'),
    )
    type = models.CharField(max_length=20, choices=TYPES, default='machine')

    def __str__(self):
        if self.type == 'machine':
            type = 'Machine à laver'
        else:
            type = 'Sèche linge'
        return type + " " + str(self.id)

    def add_interesse(self):
        self.interesses += 1
        self.save()

    def remove_interesse(self):
        self.interesses -= 1
        self.save()

    def actualiser(self):
        temps_restant = self.temps_restant = self.heure_fin - timezone.now()
        if self.libre:
            if temps_restant.days >= 0:
                self.libre = False
        else:
            if temps_restant.days >= 0:
                self.temps_restant = temps_restant
            else:
                self.libre = True
                self.temps_restant = timezone.timedelta()
        self.save()

    def get_minutes_restantes(self):
        return (60+self.temps_restant.seconds)//60

    def reste_longtemps(self):
        return self.get_minutes_restantes() > 15


class Utilisation(models.Model):
    appareil = models.ForeignKey(Appareil, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.date)







