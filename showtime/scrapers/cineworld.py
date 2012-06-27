import collections
from lxml import etree
import requests

ROOT_URL = 'http://www.cineworld.co.uk/cinemas/23'
CINEMA_URL = 'http://www.cineworld.co.uk/cinemas/{}'

Showtime = collections.namedtuple('Showtime', 'title date time')

def parse_cinema_ids(html):
    html = etree.HTML(html)
    for option in html.xpath('//select[@id="cinema"]/option'):
        id_ = option.get('value')
        if id_.isdigit():
            yield int(id_)

def parse_cinema(html):
    html = etree.HTML(html)
    for film in html.findall('.//li[@class="film-detail"]'):
        title = ''.join(film.find('.//h3[@class="filmtitle"]').itertext()).strip()
        tt = film.find('.//div[@class="timetable"]')
        for dl in tt.findall('dl'):
            date = dl.find('dt').text
            for time in dl.findall('dd/span'):
                yield Showtime(title, date, time.text)
            for time in dl.findall('dd/a'):
                yield Showtime(title, date, time.text)

#ids = parse_cinema_ids(requests.get(ROOT_URL).content)
print parse_cinema(requests.get(CINEMA_URL.format(23)).content).next()
