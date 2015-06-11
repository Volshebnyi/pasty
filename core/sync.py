from datetime import datetime
import os
import re
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

            if self.source.sync_date and self.source.sync_date >= sync_date:
                print('source is already up to date')
                return
            for entry in data.entries:
                pastry = self.parse_entry(sync_date, self.source, entry)
                # Save only if pastry is newer than previous sync date
                if pastry and (not self.source.sync_date or pastry.date > self.source.sync_date):
                    pastry.save()
                    print('saved pastry %s' % pastry)
            self.source.sync_date = sync_date
            self.source.save()
            print('successful sync for date %s' % sync_date)
        except Exception as e:
            print('sync failed: %s' % e)
            raise

    def get_data(self):
        return ParserData.from_feedparser(
            feedparser.parse(self.source.sync_url))


class LiruParser(PastySourceParser):
    source_title = 'pirozhki-ru.livejournal.com'

    def parse_entry(self, sync_date, source, entry):
        p = Pasty()
        p.text = self.strip(entry['summary_detail']['value'])
        p.date = self.to_date(entry['published_parsed'])
        if not p.date:
            p.date = sync_date
        p.source = source.url
        if len(p.text) > 255:
            return None
        return p


class StishkipirozkiParser(PastySourceParser):
    source_title = 'stishkipirozhki.ru'

    def parse_entry(self, sync_date, source, entry):
        p = Pasty()
        p.text = self.strip(entry['content'][0]['value'])
        p.date = self.to_date(entry['published_parsed'])
        if not p.date:
            p.date = sync_date
        p.source = source.url
        return p


class PerashkiParser(PastySourceParser):
    source_title = 'perashki.ru'

    def parse_entry(self, sync_date, source, entry):
        raise NotImplementedError()


PARSERS = [
    PerashkiParser(),
    LiruParser(),
    StishkipirozkiParser(),
]
