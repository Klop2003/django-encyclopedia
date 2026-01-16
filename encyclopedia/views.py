from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

ARTICLES = [
    {
        "title": "Python",
        "text": "Python — это популярный язык программирования с простым синтаксисом.",
        "image": "python.png"
    },
    {
        "title": "Django",
        "text": "Django — это фреймворк для быстрого создания веб-приложений на Python.",
        "image": "django.png"
    },
    {
        "title": "HTML",
        "text": "HTML — язык разметки для создания веб-страниц.",
        "image": "html.png"
    },
]

@require_POST
def save_settings(request):
    theme = request.POST.get("theme", "light")
    response = redirect("/")
    response.set_cookie("theme", theme, max_age=60*60*24*30)
    return response

def index(request):
    theme = request.COOKIES.get("theme", "light")

    context = {
        "articles": ARTICLES,
        "theme": theme,
    }

    response = render(request, "index.html", context)
    return response

def set_theme(request, theme):
    response = redirect("/")
    response.set_cookie("theme", theme, max_age=60*60*24*30)
    return response
