from datetime import datetime
import os
import re
import urllib2

import feedparser

from core.models import Pasty, Source


class ParseError(Exception):
    pass


class ParserData(object):
    def __init__(self, entries, date):
        self.entries = entries
        self.date = date

    @classmethod
    def from_feedparser(cls, data):
        date = datetime.now()
        if hasattr(data.feed, 'updated_parsed'):
            date = PastySourceParser.to_date(data.feed.updated_parsed)

        return cls(data.entries, date)


class PastySourceParser(object):
    source_title = None

    def __init__(self):
        self.source = Source.objects.get(title=self.source_title)

    def parse_entry(self, sync_date, source, entry):
        raise NotImplementedError()

    @staticmethod
    def strip(text):
        strip_pattern = re.compile('</?p>|</?div>')
        br_pattern = re.compile('<br ?/?>')
        space_pattern = re.compile('\s\s+')
        text = strip_pattern.sub('', text)
        text = space_pattern.sub(' ', text)
        text = br_pattern.sub(os.linesep, text)
        return text

    @staticmethod
    def to_date(feed_date):
        if not feed_date:
            return None
        return datetime(*feed_date[:6])

    def parse(self):
        print('feeding data from ' + self.source.title)
        try:
            data = self.get_data()

            sync_date = datetime.now()
            sync_date = data.date

            print len(data.entries), self.source.sync_date

            if self.source.sync_date and self.source.sync_date >= sync_date:
                print('source is already up to date')
                return

            for entry in data.entries:
                pasty = self.parse_entry(entry)
                # Save only if pasty is newer than previous sync date
                if pasty and self.is_new_pasty(pasty):
                    pasty.save()
                    print('saved pasty %s' % pasty)

            self.source.sync_date = sync_date
            self.source.save()
            print('successful sync for date %s' % sync_date)
        except Exception as e:
            print('sync failed: %s' % e)
            raise

    def get_data(self):
        return ParserData.from_feedparser(
            feedparser.parse(self.source.sync_url))

    def is_new_pasty(self, pasty):
        if self.source.sync_date is None:
            return True

        return pasty.date >= self.source.sync_date


class LiruParser(PastySourceParser):
    source_title = 'pirozhki-ru.livejournal.com'

    def parse_entry(self, entry):
        p = Pasty()
        p.text = self.strip(entry['summary_detail']['value'])
        p.date = self.to_date(entry['published_parsed'])
        if not p.date:
            p.date = self.source.sync_date
        p.source = self.source.url

        if len(p.text) > 255:
            return None
        return p


class StishkipirozkiParser(PastySourceParser):
    source_title = 'stishkipirozhki.ru'

    def parse_entry(self, entry):
        p = Pasty()
        p.text = self.strip(entry['summary_detail']['value'])
        p.date = self.to_date(entry['published_parsed'])
        if not p.date:
            p.date = self.source.sync_date
        p.source = self.source.url
        return p


class PerashkiParser(PastySourceParser):
    source_title = 'perashki.ru'
    re_pasty = (
        r'<div class="Text">([^<]+)</div>\s+'
        r'<div class="Author"><a [^<]+</a>, '
        r'<span class="date" title="\S+">(\S+)</span></div>'
    )

    def parse_entry(self, entry):
        # fake sync_date to remove duplicates

        text, date = entry
        p = Pasty()
        p.text = self.strip(text)

        # set latest time possible for proper sync
        date = datetime.strptime(date, '%d.%m.%Y')
        date = date.replace(hour=23, minute=59, second=59)
        p.date = date

        p.source = self.source.url
        return p

    def get_data(self):
        # goddamit
        # ok, let's parse HTML with regexps
        entries = []
        html = urllib2.urlopen(self.source.sync_url).read().decode('utf8')
        for m in re.findall(self.re_pasty, html, re.MULTILINE):
            entries.append(m)

        return ParserData(entries, datetime.now())

    def is_new_pasty(self, pasty):
        if self.source.sync_date is None:
            return True

        if pasty.date < self.source.sync_date:
            return False

        # directly compare today entries to prevent duplicates
        for today_pasty in Pasty.objects.filter(date=pasty.date):
            if today_pasty.text == pasty.text:
                return False

        return True


PARSERS = [
    PerashkiParser(),
    LiruParser(),
    StishkipirozkiParser(),
]
