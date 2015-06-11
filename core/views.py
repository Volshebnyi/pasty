# -*- coding: utf-8 -*-

import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import sync_rss_source


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
        sources_id = request.POST.getlist('source')
        for src_id in sources_id:
            source = Source.objects.get(pk=src_id)
            sync_rss_source(source)
    return HttpResponseRedirect(reverse('sources'))
