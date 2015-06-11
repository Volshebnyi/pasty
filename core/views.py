# -*- coding: utf-8 -*-

import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import sync_rss_source


def home(request):
    entry = Pasty.rnd()
    return render(request, 'core/home.html', {
        "entry": entry,
    })


def sources(request):
    sources = Source.objects.all()
    context = {'sources': sources}
    return render(request, 'core/sync.html', context)


def sync(request):
    sources_id = request.POST.getlist('source')
    if sources_id:
        for src_id in sources_id:
            source = Source.objects.get(pk=src_id)
            sync_rss_source(source)
    return HttpResponseRedirect(reverse('sources'))
