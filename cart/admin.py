from django.contrib import admin
from .models import *
admin.site.register(projects)
admin.site.register(full_user)
admin.site.register(comments)

# @admin.register(projects)
# class ProjectsAdmim(admin.ModelAdmin):
#     list_display = ['pname','image']
# Register your models here.
