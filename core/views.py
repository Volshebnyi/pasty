# -*- coding: utf-8 -*-

import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import sync_rss_source


def home(request):
    context = {}
    return render(request, 'core/home.html', context)


def one(request):
    p = Pasty.rnd()
    if p:
        context = {'text': p.text, 'source': p.source, 'title': p.source_title()}
        return render(request, 'core/pasty.html', context)
    else:
        return HttpResponse(u'<div class="box pasty">Нету пирожков :-(</div>')


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
