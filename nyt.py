from urllib2 import urlopen, HTTPError
from json import JSONDecoder, JSONEncoder
from datetime import datetime, timedelta
import sys

def daterange(start_date, end_date):
    for n in xrange(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

parse_date = lambda s: datetime.strptime(s, "%Y-%m-%dT%XZ")

decoder = JSONDecoder()
encoder = JSONEncoder()
objs = []
url_format = 'http://query.nytimes.com/svc/cse/v2/sitesearch.json?date_range_upper=%(date)s&date_range_lower=%(date)s&vertical=politics&sort_order=a&page=%(page)d' 
written = True
if not written:
    sys.stdout.write('[')
with open('nyt.log','a') as f, open('nyturls.txt','a') as u:
    for current_date in daterange(datetime(2000,1,1), datetime(2013,8,24)):
        page = 0
        while True:
            url_to_fetch = url_format % {
                'date': current_date.strftime('%Y%m%d'),
                'page': page
            }
            try:
                json = urlopen(url_to_fetch).read()
            except HTTPError:
                sys.stderr.write('error on current_date date %s, url=%s\n' % \
                                (current_date, url_to_fetch))
                continue
            results = decoder.decode(json)[u'results']
            docs = results[u'results']
            for doc in docs:
                u.write(doc[u'url'] + '\n')
                if u'xlarge' not in doc:
                    continue
                if written:
                    sys.stdout.write(',\n')
                sys.stdout.write(encoder.encode({
                    u'headline': doc[u'hdl'],
                    u'extended_headline': doc.get(u'hdl_p', None),
                    u'source': doc.get(u'cre', 'nytimes.com'),
                    u'url': doc[u'url'],
                    u'date': current_date.strftime('%Y/%m/%d'),
                    u'imgUrl': doc[u'xlarge'],
                    u'dimensions': (doc.get(u'xlarge_height'), doc.get(u'xlarge_width')),
                    u'placement': u'top'
                }))
                written = True
            metadata = results[u'meta']
            if metadata[u'results_end'] == metadata[u'results_estimated_total']:
                num_results = int(metadata[u'results_estimated_total'] or 0)
                f.write('date=%s, count=%d\n' % (current_date.isoformat(),
                                                 num_results))
                break
            page += 1
sys.stdout.write(']')
