# -*- coding: utf-8 -*-

from django import forms


class AddForm(forms.Form):
    text = forms.CharField(
        label=u'Текст пирожка',
        max_length=100,
        widget=forms.Textarea)
    source = forms.CharField(label=u'Источник', max_length=100, initial='Наша компания')
    votes = forms.IntegerField(
        label=u'Голоса (чем больше - тем чаще показывается)',
        initial='100')
