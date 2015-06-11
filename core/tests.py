"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase

import sync
import models


class SimpleTest(TestCase):
    def test_parse_liru(self):
        sync.LiruParser().parse()
        self.assertTrue(models.Pasty.objects.all())

    def test_parse_stishki(self):
        sync.StishkipirozkiParser().parse()
        self.assertTrue(models.Pasty.objects.all())

    def test_parse_perashki(self):
        sync.PerashkiParser().parse()
        self.assertTrue(models.Pasty.objects.all())

    def test_parse_liru_entry(self):
        entry = {'summary_detail': {'base': u'http://pirozhki-ru.livejournal.com/data/rss', 'type': u'text/html', 'value': u'\u0438\u0434\u0443\u0442 \u0432\u0430\u043d\u0434\u0430\u043b \u0441 \u0430\u043d\u0442\u0438\u0432\u0430\u043d\u0434\u0430\u043b\u043e\u043c <br />\u0432\u0434\u0440\u0443\u0433 \u0443\u0440\u043d\u0430 \u0441 \u0433\u0438\u0442\u043b\u0435\u0440\u043e\u043c \u043e\u043d\u0438<br />\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u043b\u0438\u0441\u044c \u0434\u0440\u0443\u0433 \u043d\u0430 \u0434\u0440\u0443\u0433\u0430<br />\u0433\u043b\u044f\u0434\u044f\u0442 \u043b\u0430\u0441\u043a\u0430\u044f \u043f\u0438\u0441\u0442\u043e\u043b\u044c\u0442\u044b', 'language': None}, 'published_parsed': (2014, 7, 23, 23, 56, 5, 2, 204, 0), 'links': [{'href': u'http://pirozhki-ru.livejournal.com/1671972.html', 'type': u'text/html', 'rel': u'alternate'}], u'lj_security': u'public', u'lj_poster': u'kvatanastini', 'comments': u'http://pirozhki-ru.livejournal.com/1671972.html', 'summary': u'\u0438\u0434\u0443\u0442 \u0432\u0430\u043d\u0434\u0430\u043b \u0441 \u0430\u043d\u0442\u0438\u0432\u0430\u043d\u0434\u0430\u043b\u043e\u043c <br />\u0432\u0434\u0440\u0443\u0433 \u0443\u0440\u043d\u0430 \u0441 \u0433\u0438\u0442\u043b\u0435\u0440\u043e\u043c \u043e\u043d\u0438<br />\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u043b\u0438\u0441\u044c \u0434\u0440\u0443\u0433 \u043d\u0430 \u0434\u0440\u0443\u0433\u0430<br />\u0433\u043b\u044f\u0434\u044f\u0442 \u043b\u0430\u0441\u043a\u0430\u044f \u043f\u0438\u0441\u0442\u043e\u043b\u044c\u0442\u044b', 'guidislink': True, 'link': u'http://pirozhki-ru.livejournal.com/1671972.html', u'lj_posterid': u'27360425', 'published': u'Wed, 23 Jul 2014 23:56:05 GMT', u'lj_reply-count': u'5', 'id': u'http://pirozhki-ru.livejournal.com/1671972.html'}
        pasty = sync.LiruParser().parse_entry(entry)
        self.assertTrue(pasty)

    def test_parse_stishki_entry(self):
        entry = {'summary_detail': {'base': u'http://www.stishkipirozhki.ru/rss/', 'type': u'application/xhtml+xml', 'value': u'\u043a\u0432\u0430\u0434\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u0432\u0438\u0447\u0430 \u0441\u0447\u0438\u0442\u0430\u044e\u0442<br /> \u043a\u043e\u043d\u0433\u0435\u043d\u0438\u0430\u043b\u044c\u043d\u044b\u043c \u043d\u043e \u043f\u043e \u043c\u043d\u0435<br /> \u043a\u0440\u0443\u0433 \u0434\u0436\u043e\u0442\u0442\u043e \u0431\u044b\u043b \u043f\u043e\u0438\u0434\u0435\u0430\u043b\u044c\u043d\u0435\u0439<br /> \u043d\u043e \u0432\u0430\u043c \u043a\u043e\u043d\u0435\u0447\u043d\u043e \u0432\u0441\u0451 \u0440\u0430\u0432\u043d\u043e', 'language': None}, 'published_parsed': (2015, 5, 13, 17, 57, 46, 2, 133, 0), 'links': [{'href': u'http://www.stishkipirozhki.ru/rss/www.stishkipirozhki.ru/', 'type': u'text/html', 'rel': u'alternate'}], 'title': u'\u043a\u0432\u0430\u0434\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u0432\u0438\u0447\u0430 \u0441\u0447\u0438\u0442\u0430\u044e\u0442 \u043a\u043e\u043d\u0433\u0435\u043d\u0438\u0430\u043b\u044c\u043d\u044b\u043c \u043d\u043e \u043f\u043e \u043c\u043d\u0435 \u043a\u0440\u0443\u0433 \u0434\u0436\u043e\u0442\u0442\u043e \u0431\u044b\u043b \u043f\u043e\u0438\u0434\u0435\u0430\u043b\u044c\u043d\u0435\u0439 \u043d\u043e \u0432\u0430\u043c \u043a\u043e\u043d\u0435\u0447\u043d\u043e \u0432\u0441\u0451 \u0440\u0430\u0432\u043d\u043e', 'author': u'\u041c\u0430\u0440\u044b\u0441\u044f', 'summary': u'\u043a\u0432\u0430\u0434\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u0432\u0438\u0447\u0430 \u0441\u0447\u0438\u0442\u0430\u044e\u0442<br /> \u043a\u043e\u043d\u0433\u0435\u043d\u0438\u0430\u043b\u044c\u043d\u044b\u043c \u043d\u043e \u043f\u043e \u043c\u043d\u0435<br /> \u043a\u0440\u0443\u0433 \u0434\u0436\u043e\u0442\u0442\u043e \u0431\u044b\u043b \u043f\u043e\u0438\u0434\u0435\u0430\u043b\u044c\u043d\u0435\u0439<br /> \u043d\u043e \u0432\u0430\u043c \u043a\u043e\u043d\u0435\u0447\u043d\u043e \u0432\u0441\u0451 \u0440\u0430\u0432\u043d\u043e', 'guidislink': False, 'title_detail': {'base': u'http://www.stishkipirozhki.ru/rss/', 'type': u'text/plain', 'value': u'\u043a\u0432\u0430\u0434\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u0432\u0438\u0447\u0430 \u0441\u0447\u0438\u0442\u0430\u044e\u0442 \u043a\u043e\u043d\u0433\u0435\u043d\u0438\u0430\u043b\u044c\u043d\u044b\u043c \u043d\u043e \u043f\u043e \u043c\u043d\u0435 \u043a\u0440\u0443\u0433 \u0434\u0436\u043e\u0442\u0442\u043e \u0431\u044b\u043b \u043f\u043e\u0438\u0434\u0435\u0430\u043b\u044c\u043d\u0435\u0439 \u043d\u043e \u0432\u0430\u043c \u043a\u043e\u043d\u0435\u0447\u043d\u043e \u0432\u0441\u0451 \u0440\u0430\u0432\u043d\u043e', 'language': None}, 'link': u'http://www.stishkipirozhki.ru/rss/www.stishkipirozhki.ru/', 'authors': [{}], 'author_detail': {'name': u'\u041c\u0430\u0440\u044b\u0441\u044f'}, 'id': u'http://www.stishkipirozhki.ru/rss/www.stishkipirozhki.ru/', 'published': u'2015-05-13 17:57:46'}
        pasty = sync.StishkipirozkiParser().parse_entry(entry)
        self.assertTrue(pasty)

    def test_parse_perashki_entry(self):
        entry = (u'\u043d\u0430 \u043f\u043b\u043e\u0449\u0430\u0434\u0438 \u0443\u0432\u0438\u0434\u0435\u043b \u0434\u0440\u0443\u0433\u0430 \r\n\u043d\u0435 \u0443\u0434\u0435\u0440\u0436\u0430\u043b\u0441\u044f \u0437\u0430\u043a\u0443\u0440\u0438\u043b \r\n\u0441\u043e\u0432\u0441\u0435\u043c \u043c\u043e\u0439 \u0434\u0440\u0443\u0433 \u043d\u0435 \u0438\u0437\u043c\u0435\u043d\u0438\u043b\u0441\u044f \r\n\u043b\u0438\u0448\u044c \u0448\u043b\u0451\u043c \u0441\u043b\u0435\u0433\u043a\u0430 \u043f\u043e\u0437\u0435\u043b\u0435\u043d\u0435\u043b', u'05.06.2015')
        pasty = sync.PerashkiParser().parse_entry(entry)
        self.assertTrue(pasty)
