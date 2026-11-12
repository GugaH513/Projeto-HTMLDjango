# ATV09 — Migração do Portal para Django

**Dupla:** Gustavo Henrique Malta Ferreira e Alex Fernandes de Araújo Leite — Turma 513 (IFAL)

##Descrição

Evolução do portal da ATV06 (HTML semântico, CSS, Flexbox e responsividade) para uma
aplicação **Django**. A identidade visual, o layout e as imagens foram mantidos; o que mudou:

- as páginas (currículos, Kamen Rider 555, Não Jogue, Notícias) agora são registros do model `Conteudo`;
- o menu é gerado dinamicamente a partir do model `Menu` (itens internos e links externos);
- tudo é administrável pelo **Django Admin**;
- a navegação usa URLs e Views do Django (o `fetch()` em JavaScript da ATV06 foi substituído).

## Tecnologias

Python 3 · Django 5.2 · SQLite · HTML5 · CSS3 (Flexbox/Grid/Media Queries) · Git/GitHub

## Estrutura

```
ATV09_Gustavo_Alex/
├── manage.py
├── portal/                  # projeto Django (settings, urls)
└── core/                    # aplicação
    ├── models.py            # Conteudo e Menu
    ├── admin.py             # registro dos models no Admin
    ├── views.py             # pagina_inicial, exibir_conteudo, obter_itens_menu
    ├── urls.py              # "/" e "/conteudo/<slug>/"
    ├── migrations/
    ├── templates/core/      # base.html, home.html, conteudo.html
    ├── static/core/         # css/style.css e img/
    ├── conteudos_iniciais/  # HTML dos conteúdos (usado para popular o banco)
    └── management/commands/popular_portal.py
```

## Como executar

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Criar o banco (migrations)
python manage.py migrate

# 4. Cadastrar os conteúdos e itens de menu iniciais
python manage.py popular_portal

# 5. Criar o superusuário (acesso ao Admin)
python manage.py createsuperuser

# 6. Rodar o servidor
python manage.py runserver
```

## Acessos

- Portal: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/

## Como funciona (resumo)

- **Conteudo**: `titulo`, `slug` (único), `conteudo_html` (somente o HTML interno), `ativo`.
- **Menu**: `titulo`, `tipo_destino` (interno/externo), `ordem`, `ativo`, `conteudo` (FK, quando interno) e `url_externa` (quando externo). O método `clean()` valida que o destino combina com o tipo.
- O template `base.html` percorre `itens_menu` (enviado pela view) e monta o `<nav>`.
- Imagens e CSS ficam em `core/static/core/`; o HTML do banco referencia `/static/core/img/...`.
