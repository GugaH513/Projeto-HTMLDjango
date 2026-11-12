from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Conteudo(models.Model):
    """Página de conteúdo do portal.

    Guarda apenas o HTML *interno* da página. A estrutura principal
    (html, head, body, header, nav, footer) fica nos templates Django.
    """

    titulo = models.CharField("título", max_length=150)
    slug = models.SlugField(
        "slug",
        max_length=150,
        unique=True,
        help_text="Usado na URL: /conteudo/<slug>/",
    )
    conteudo_html = models.TextField(
        "conteúdo HTML",
        help_text="Somente o HTML interno da página (sem html, head, body, header, nav ou footer).",
    )
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "conteúdo"
        verbose_name_plural = "conteúdos"
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("conteudo", kwargs={"slug": self.slug})


class Menu(models.Model):
    """Item da navegação do portal (interno ou externo)."""

    class Destino(models.TextChoices):
        INTERNO = "interno", "Conteúdo interno"
        EXTERNO = "externo", "Link externo"

    titulo = models.CharField("título", max_length=100)
    tipo_destino = models.CharField(
        "tipo de destino",
        max_length=10,
        choices=Destino.choices,
        default=Destino.INTERNO,
    )
    ordem = models.PositiveIntegerField(
        "ordem", default=0, help_text="Menor número aparece primeiro."
    )
    ativo = models.BooleanField("ativo", default=True)
    conteudo = models.ForeignKey(
        Conteudo,
        verbose_name="conteúdo relacionado",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="itens_menu",
        help_text="Obrigatório quando o destino for 'Conteúdo interno'.",
    )
    url_externa = models.URLField(
        "URL externa",
        blank=True,
        help_text="Obrigatória quando o destino for 'Link externo'.",
    )

    class Meta:
        verbose_name = "item de menu"
        verbose_name_plural = "itens de menu"
        ordering = ["ordem", "titulo"]

    def __str__(self):
        return self.titulo

    @property
    def eh_externo(self):
        return self.tipo_destino == self.Destino.EXTERNO

    def clean(self):
        """Garante que o item tenha o destino coerente com o tipo escolhido."""
        if self.tipo_destino == self.Destino.INTERNO:
            if self.conteudo_id is None:
                raise ValidationError(
                    {"conteudo": "Selecione o conteúdo para um item de destino interno."}
                )
            self.url_externa = ""
        elif self.tipo_destino == self.Destino.EXTERNO:
            if not self.url_externa:
                raise ValidationError(
                    {"url_externa": "Informe a URL para um item de destino externo."}
                )
            self.conteudo = None

    def get_url(self):
        """Retorna a URL final do item (usa o sistema de URLs do Django)."""
        if self.eh_externo:
            return self.url_externa
        if self.conteudo is None:
            return "#"
        if self.conteudo.slug == settings.SLUG_PAGINA_INICIAL:
            return reverse("home")
        return self.conteudo.get_absolute_url()
