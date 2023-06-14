import aiohttp
from bs4 import BeautifulSoup
import asyncio

class AsyncWebScraper:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    async def login(self, session):
        # The payload should match the form fields for the website
        payload = {
            'username': self.username,
            'password': self.password
        }
        await session.post(self.url, data=payload)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self):
        async with aiohttp.ClientSession() as session:
            await self.login(session)
            html = await self.fetch(session, self.url)
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', {'class': 'content'})

            if content:
                h3 = content.find('h3')

                if h3 and 'Бакалавриат' in h3.text:
                    aalink = content.find('a', {'class': 'aalink'})

                    if aalink and 'href' in aalink.attrs:
                        href = aalink['href']
                        # Follow the link
                        html = await self.fetch(session, href)

                        # Process the new page
                        soup = BeautifulSoup(html, 'html.parser')
                        span = soup.find('span', {'class': 'fp-filename-icon'})

                        if span:
                            a = span.find('a')

                            if a and 'href' in a.attrs:
                                return a['href']
            return None


# Use the class
scraper = AsyncWebScraper('https://edu.stankin.ru', 'st317097', 'NoviySvit2015')

loop = asyncio.get_event_loop()
result = loop.run_until_complete(scraper.main())

print(result)
