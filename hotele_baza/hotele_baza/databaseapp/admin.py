from django.contrib import admin

from .models import Users
from .models import Hotels
from .models import Locations
from .models import Reservations
from .models import Rooms
admin.site.register(Users)
admin.site.register(Hotels)
admin.site.register(Locations)
admin.site.register(Reservations)
admin.site.register(Rooms)