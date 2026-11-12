from django import forms
from django.contrib import admin

from .models import Conteudo, Menu


@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "slug", "ativo")
    list_filter = ("ativo",)
    list_editable = ("ativo",)
    search_fields = ("titulo", "slug")
    prepopulated_fields = {"slug": ("titulo",)}
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "conteudo_html":
            field.widget = forms.Textarea(
                attrs={"rows": 30, "cols": 120, "style": "font-family: monospace;"}
            )
        return field


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_destino", "conteudo", "url_externa", "ordem", "ativo")
    list_filter = ("tipo_destino", "ativo")
    list_editable = ("ordem", "ativo")
    search_fields = ("titulo",)
    ordering = ("ordem", "titulo")
