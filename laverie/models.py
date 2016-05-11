from django.db import models


class Appareil(models.Model):
    temps_max = models.IntegerField(default=50)
    temps_restant = models.IntegerField(default=0)
    interesses = models.IntegerField(default=0)
    libre = models.BooleanField(default=True)
    TYPES = (
        ('machine', 'Machine à laver'),
        ('seche_linge', 'Sèche linge'),
    )
    type = models.CharField(max_length=20, choices=TYPES)
    compteur_actif = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" %(self.type, self.id)

    def est_libre(self):
        self.libre = self.temps_restant == 0
        self.save()
        return self.libre

    def add_interesse(self):
        self.interesses += 1

    def remove_interesse(self):
        self.interesses -= 1



