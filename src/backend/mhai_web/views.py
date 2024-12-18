from django.shortcuts import render
from stronghold.decorators import public


@public
def index(request):
    return render(request, "pages/home.html")
