from django.shortcuts import render


def index(request):
    template = 'includes/index.html'
    return render(request, template)
