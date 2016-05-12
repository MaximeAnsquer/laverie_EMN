from django.contrib import admin
from .models import Appareil
from .models import Utilisation

admin.site.register(Appareil)
admin.site.register(Utilisation)
