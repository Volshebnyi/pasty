# -*- coding: utf-8 -*-

import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from core.models import Pasty
from core.models import Source
from core.sync import PARSERS

import forms


@login_required
def home(request):
    return render(request, 'core/home.html')


def kiosk(request):
    return render(request, 'core/kiosk.html', {
        "pasty": Pasty.rnd(),
    })


@login_required
def add_entry(request):
    if request.POST:
        form = forms.AddForm(request.POST)
        if form.is_valid():
            pasty = Pasty(
                text=form.cleaned_data['text'],
                source_title=form.cleaned_data['source_title'],
                date=datetime.datetime.now(),
                votes=form.cleaned_data['votes'],
            )
            pasty.save()
            return HttpResponseRedirect(reverse('add_success'))
    else:
        form = forms.AddForm()

    return render(request, 'core/add.html', {
        'sources': Source.objects.all(),
        'form': forms.AddForm(),
    })


@login_required
def add_success(request):
    return render(request, 'core/success.html')


@login_required
def sync(request):
    if request.POST:
        sources_id = [int(i) for i in request.POST.getlist('source')]
        for parser in PARSERS:
            if parser.source.id in sources_id:
                parser.parse()

    return render(request, 'core/sync.html', {
        'sources': Source.objects.all(),
    })


def login(request):
    return HttpResponseRedirect(reverse('admin:index'))
