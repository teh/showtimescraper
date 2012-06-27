import collections
from lxml import etree
import requests

ROOT_URL = 'http://www.empirecinemas.co.uk/index.php?page=nowshowing&tbx_site_id={cinema_id:d}'

Showtime = collections.namedtuple('Showtime', 'title date time')

def parse_cinema_ids(html):
    html = etree.HTML(html)
    for option in html.xpath('//select[@name="tbx_site_id"]/option'):
        id_ = option.get('value')
        if id_.isdigit():
            yield int(id_)
    return result

def parse_cinema(html):
    html = etree.HTML(html)
    for a in html.xpath('//ul[@class="filmlist"]/li/a'):
        full = a.get('title')
        # e.g.
        # Book tickets for "Friends With Kids" on Wednesday  4/07/12 at 15:45
        _, title, date_string = full.split('"')
        _, _, uk_date, _, time = date_string.split()
        yield Showtime(title, uk_date, time)

#ids = parse_cinema_ids(requests.get(ROOT_URL.format(cinema_id=5)).content)
print parse_cinema(requests.get(ROOT_URL.format(cinema_id=5)).content)
