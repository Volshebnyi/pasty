# -*- coding: utf-8 -*-

import os
import re
import random
from urlparse import urlparse

from django.db import models


class Pasty(models.Model):
    text = models.TextField(u'Текст пирожка')
    date = models.DateTimeField(u'Дата публикации', blank=True, null=True)
    source = models.URLField(u'Источник', blank=True)
    votes = models.IntegerField(u'Голосов', default=0, null=True)
    source_pattern = re.compile(r'''http://(?:www\.)?(.+)''')

    def short_text(self):
        return self.text[:37].replace(os.linesep, ' \ ') + '...'

    @property
    def source_title(self):
        return urlparse(self.source).hostname

    def __unicode__(self):
        return self.short_text()

    @staticmethod
    def rnd():
        if Pasty.objects.count() == 0:
            return None

        # random weighted choice here
        candidates = Pasty.objects.order_by('?')[:5]

        # give not so popular pasties some chance!
        votes_handicap = 100
        votes_min = min([i.votes for i in candidates])
        choices = [(i, i.votes - votes_min + votes_handicap) for i in candidates]

        total = sum(weight for item, weight in choices)
        r = random.uniform(0, total)
        upto = 0
        for item, weight in choices:
            if upto + weight > r:
                return item
            upto += weight

        # this never happen
        return None


class Source(models.Model):
    title = models.TextField(u'Название источника')
    url = models.URLField(u'Ссылка')
    sync_url = models.URLField(u'URL синхронизации', blank=True)
    sync_date = models.DateTimeField(u'Дата последней синхронизации', blank=True, null=True)
    parser_pattern = re.compile('[.-]')

    def __unicode__(self):
        return self.title

    def parser(self):
        return self.parser_pattern.sub('_', self.title)
