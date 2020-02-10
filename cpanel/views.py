from django.shortcuts import render
from django.http import HttpResponse


def mainRTL(request):
    context = {
        'title': 'BaseRTL',
    }
    return render(request, 'cpanel/base-rtl.html', context)


def main(request):
    context = {
        'title': 'base',
    }
    return render(request, 'cpanel/base.html', context)
