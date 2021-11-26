from django.contrib import admin
from .models import *

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('username',
    'code', 'created')

    search_fields = ('username', 'code',)
