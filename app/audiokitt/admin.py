from django.contrib import admin

from .models import Analyse, Inquiry


class BaseAdmin(admin.ModelAdmin):

    save_on_top = True


@admin.register(Inquiry)
class InquiryAdmin(BaseAdmin):

    list_display = [
        '__str__',
        'user',
        'uuid',
        'created',
        'status',
    ]

    list_filter = [
        'created',
        'analyse__status',
    ]




admin.site.register(Analyse)
