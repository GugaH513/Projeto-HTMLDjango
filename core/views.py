from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import Conteudo, Menu


def obter_itens_menu():
    """Busca no banco os itens ativos do menu, já ordenados."""
    return Menu.objects.filter(ativo=True).select_related("conteudo").order_by("ordem", "titulo")


def pagina_inicial(request):
    """Página inicial: exibe o Conteudo cujo slug está em SLUG_PAGINA_INICIAL."""
    slug = settings.SLUG_PAGINA_INICIAL
    conteudo = Conteudo.objects.filter(slug=slug, ativo=True).first()
    return render(
        request,
        "core/home.html",
        {
            "itens_menu": obter_itens_menu(),
            "conteudo": conteudo,
            "slug_atual": slug,
        },
    )


def exibir_conteudo(request, slug):
    """Exibe um Conteudo ativo a partir do slug da URL (404 se não existir)."""
    conteudo = get_object_or_404(Conteudo, slug=slug, ativo=True)
    return render(
        request,
        "core/conteudo.html",
        {
            "itens_menu": obter_itens_menu(),
            "conteudo": conteudo,
            "slug_atual": conteudo.slug,
        },
    )
