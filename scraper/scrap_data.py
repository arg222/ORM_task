import aiohttp
import asyncio
import requests
import lxml

from bs4 import BeautifulSoup
from models import Movies

movies_name = []
actors_name = []
date_of_issue = []
genres = []
rates = []
list_data = []


def get_urls(url: str, url_count: int):
    for num in range(1, url_count + 1):
        list_data.append(f'{url}?page={num}')
    return list_data


async def async_parse(url: str):
    session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=50)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.get(url) as req:
            data = await req.text()
            async_parse_data(data)


def async_parse_data(html_single_page):
    soup = BeautifulSoup(html_single_page, 'lxml')
    movies = soup.find_all('div', attrs={'class': 'movie'})
    for movie in movies:
        movie_href = movie.find('a')['href']
        req_movie = requests.get(f'https://www.kinokopilka.pro{movie_href}').text
        soup_ = BeautifulSoup(req_movie, 'lxml')
        movie_fields = soup_.find('div', attrs={'class': 'block view'})
        movies_name.append(movie_fields.h1.text)
        data = movie_fields.find_all('li', attrs={'class': ''})
        genres.append(data[0].text.strip().split()[1:])
        date_of_issue.append(data[1].text.strip().split()[-1])
        rate_ = movie_fields.find('span', attrs={"itemprop": "ratingValue"})
        if rate_ is not None:
            rates.append(rate_.text)
        else:
            rates.append(5.5)
        actors = soup_.find_all('div', attrs={'class': 'person'})
        d = []
        for actor in actors:
            d.append(actor.a['title'])
        actors_name.append(d)


def set_db():

    movies_data_list = [i for i in zip(movies_name[1:], actors_name[1:], genres[1:], date_of_issue[1:], rates[1:])]
    movies_fields = ('movies_name', 'actors_name', 'genres', 'date_of_issue', 'rates')
    Movies.object.insert_many(movies_fields, movies_data_list)
    # movies_data_list_not_all = [i for i in zip(movies_name[1:], genres[1:], date_of_issue[1:], rates[1:])]
    # movies_fields_not_all = ('movies_name', 'genres', 'date_of_issue', 'rates')
    # Movies.object.insert_many(movies_fields_not_all, movies_data_list_not_all)


if __name__ == '__main__':
    list_data = get_urls('https://www.kinokopilka.pro/', 5)
    event_loop = asyncio.new_event_loop()
    tasks = [event_loop.create_task(async_parse(url)) for url in list_data]
    event_loop.run_until_complete(asyncio.wait(tasks))
    set_db()
