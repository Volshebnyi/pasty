# -*- coding: utf-8 -*-

import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import PARSERS

import forms


def home(request):
    return render(request, 'core/home.html', {
        "pasty": Pasty.rnd(),
    })


def add_entry(request):
    if request.POST:
        form = forms.AddForm(request.POST)
        if form.is_valid():
            pasty = Pasty(
                text=form.cleaned_data['text'],
                source=form.cleaned_data['source'],
                date=datetime.datetime.now(),
                votes=form.cleaned_data['votes'],
            )
            pasty.save()
    else:
        form = forms.AddForm()

    return render(request, 'core/add.html', {
        'sources': Source.objects.all(),
        'form': forms.AddForm(),
    })


def sync(request):
    if request.POST:
        sources_id = [int(i) for i in request.POST.getlist('source')]
        for parser in PARSERS:
            if parser.source.id in sources_id:
                parser.parse()

    return render(request, 'core/sync.html', {
        'sources': Source.objects.all(),
    })
