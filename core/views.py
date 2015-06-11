# -*- coding: utf-8 -*-

import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import PARSERS


def home(request):
    return render(request, 'core/home.html', {
        "pasty": Pasty.rnd(),
    })


def sources(request):
    return render(request, 'core/sync.html', {
        'sources': Source.objects.all()
    })


def sync(request):
    if request.POST:
        sources_id = [int(i) for i in request.POST.getlist('source')]
        for parser in PARSERS:
            if parser.source.id in sources_id:
                parser.parse()
    return HttpResponseRedirect(reverse('sources'))
