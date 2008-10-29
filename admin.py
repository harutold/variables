# -*- coding: utf-8 -*-
from django.contrib import admin
from django_utils import AdminWYSIWYG
from models import Variable

class VariableAdmin(AdminWYSIWYG):
    list_display = ('name', 'desc')

admin.site.register(Variable, VariableAdmin)
