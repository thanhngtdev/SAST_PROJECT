from projects.models import Projects, Targets, Organization, Scans
from django.contrib import admin

admin.site.register(Organization)
admin.site.register(Projects)
admin.site.register(Targets)
admin.site.register(Scans)
