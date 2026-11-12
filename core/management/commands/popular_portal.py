"""Popula o banco com os conteúdos e o menu da ATV06 migrados para Django.

Uso:  python manage.py popular_portal

É seguro rodar mais de uma vez (usa update_or_create).
Os dados também podem ser criados/alterados pelo Django Admin.
"""
from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Conteudo, Menu

PASTA_HTML = Path(__file__).resolve().parents[2] / "conteudos_iniciais"

# (título, slug, arquivo .html em core/conteudos_iniciais/)
CONTEUDOS = [
    ("Início", "inicio", "inicio.html"),
    ("Currículo Alex", "curriculo-alex", "curriculo-alex.html"),
    ("Currículo Gustavo", "curriculo-gustavo", "curriculo-gustavo.html"),
    ("Kamen Rider 555", "kamen-rider-555", "kamen-rider-555.html"),
    ("Não Jogue", "nao-jogue", "nao-jogue.html"),
    ("Notícias", "noticias", "noticias.html"),
]

# (título, ordem, slug do conteúdo)  -> itens internos
MENU_INTERNO = [
    ("Início", 1, "inicio"),
    ("Currículo Alex", 2, "curriculo-alex"),
    ("Currículo Gustavo", 3, "curriculo-gustavo"),
    ("Kamen Rider 555", 4, "kamen-rider-555"),
    ("Não Jogue", 5, "nao-jogue"),
    ("Notícias", 6, "noticias"),
]

# (título, ordem, url) -> itens externos
MENU_EXTERNO = [
    ("GitHub", 7, "https://github.com/GugaH513/Projeto-HTMLDjango"),
    ("W3Schools", 8, "https://www.w3schools.com/"),
]


class Command(BaseCommand):
    help = "Cadastra os conteúdos e itens de menu iniciais do portal."

    def handle(self, *args, **options):
        objetos = {}
        for titulo, slug, arquivo in CONTEUDOS:
            html = (PASTA_HTML / arquivo).read_text(encoding="utf-8")
            obj, _ = Conteudo.objects.update_or_create(
                slug=slug,
                defaults={"titulo": titulo, "conteudo_html": html, "ativo": True},
            )
            objetos[slug] = obj

        for titulo, ordem, slug in MENU_INTERNO:
            Menu.objects.update_or_create(
                titulo=titulo,
                defaults={
                    "tipo_destino": Menu.Destino.INTERNO,
                    "ordem": ordem,
                    "ativo": True,
                    "conteudo": objetos[slug],
                    "url_externa": "",
                },
            )

        for titulo, ordem, url in MENU_EXTERNO:
            Menu.objects.update_or_create(
                titulo=titulo,
                defaults={
                    "tipo_destino": Menu.Destino.EXTERNO,
                    "ordem": ordem,
                    "ativo": True,
                    "conteudo": None,
                    "url_externa": url,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"{len(CONTEUDOS)} conteúdos e {len(MENU_INTERNO) + len(MENU_EXTERNO)} itens de menu cadastrados."
        ))
